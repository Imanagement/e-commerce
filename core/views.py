from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import BadHeaderError, send_mail
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from django.db.models import Avg, Count, Max, Min, Q
from django.db.models.functions import Coalesce
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.cache import add_never_cache_headers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.utils.html import strip_tags
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .templatetags.cart_template_tags import cart_total_summary
from .models import (
    BillingAddress,
    Brand,
    Category,
    DelieveryOption,
    CustomerRequestToCallBack,
    ExtraOption,
    ExtraOptionOrdered,
    HomePageBannerImage,
    HotProduct,
    Basket,
    BasketProduct,
    Page,
    PaymentOption,
    Product,
    ProductView,
    PropertyValue,
    ProductReview,
    Property,
    OrderedBasket,)
from .forms import CheckoutForm, LeaveTheMessageForm


class BasePage(object):

    def get_main_categories(self):
        return Category.objects.filter(parent=None, level=0).prefetch_related('category_set')

    def get_popular_products(self):
        popular_products_query = Product.objects.filter(
            views_count__isnull=False, not_in_stock=False).order_by('-views_count')[:12]
        return popular_products_query

    def get_newest_products(self):
        newest_products_query = Product.objects.filter(
            not_in_stock=False).order_by('-published')[:12]
        return newest_products_query

    def get_seo(self, request):
        try:
            seo = Page.objects.get(slug=request.path)
        except Page.DoesNotExist:
            seo = None
        return seo

    def get_cart_products(self):
        if self.request.user.is_authenticated:
            order_query = Basket.objects.filter(
                user=self.request.user, is_ordered=False)
        elif self.request.session.get('has_cart', None) == '1' and self.request.session.get('cart_id', None) is not None:
            order_query = Basket.objects.filter(
                pk=self.request.session['cart_id'], is_ordered=False)
        else:
            order_query = Basket.objects.none()
        if order_query.exists():
            basket = order_query[0]
            cart_product = basket.products.filter(
                basket=basket).select_related('product').prefetch_related('extraoptionordered_set')[:3]
        else:
            return None
        return cart_product


class HomeView(ListView, BasePage):
    model = Product
    template_name = 'core/home.html'
    context_object_name = 'products_list'
    queryset = model.objects.filter(not_in_stock=False)[:8]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_categories'] = super().get_main_categories()
        context['newest_products'] = super().get_newest_products()
        context['popular_products'] = super().get_popular_products()
        context['order_products'] = super().get_cart_products()
        context['seo'] = super().get_seo(self.request)
        context['footer_categories_with_products'] = self.get_footer_products()
        context['hot_product'] = self.get_hot_product()
        context['stocks'] = self.get_stock_products()
        context['banner_images'] = self.get_banner_images()
        return context

    def get_footer_products(self):
        categories = Category.objects.filter(
            show_on_the_homepage_at_the_footer=True, parent=None, level=0)
        categories_with_products = {}
        for category in categories:
            categories_with_products[category.name] = {}
            categories_with_products[category.name]['slug'] = category.slug
            categories_with_products[category.name]['products'] = Category.objects.none(
            )
            if category == categories[0]:
                categories_with_products[category.name]['active'] = 'active'
            for descendant in category.get_descendants():
                categories_with_products[category.name]['products'] |= Product.objects.filter(
                    category=descendant, price__gte=2000)
            categories_with_products[category.name]['products'] = categories_with_products[category.name]['products'][:12]

        return categories_with_products

    def get_hot_product(self):
        try:
            hot_products = HotProduct.objects.all().select_related('product')
            return hot_products[0]
        except Exception:
            return None

    def get_stock_products(self):
        try:
            stock_products = self.model.objects.filter(
                discount_price__isnull=False)[:8]
            return stock_products
        except Exception:
            return None

    def get_banner_images(self):
        try:
            banner_images = HomePageBannerImage.objects.all().select_related('category_follow_to')
            return banner_images
        except Exception:
            return None


class CategoryList(ListView, BasePage):
    model = Category
    template_name = 'core/main-categories.html'

    def get_queryset(self):
        parent_category = self.model.objects.get(
            slug=self.kwargs['slug'])
        return self.model.objects.filter(parent=parent_category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_category'] = self.model.objects.get(
            slug=self.kwargs['slug'])
        context['main_categories'] = super().get_main_categories()
        context['newest_products'] = super().get_newest_products()
        context['popular_products'] = super().get_popular_products()
        context['order_products'] = super().get_cart_products()
        return context


class NeverCacheMixin(object):
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(NeverCacheMixin, self).dispatch(*args, **kwargs)


class DisableClientSideCachingMiddleware(object):
    def process_response(self, request, response):
        add_never_cache_headers(response)
        return response


class CategoryView(NeverCacheMixin, DisableClientSideCachingMiddleware, ListView, BasePage):
    model = Product
    paginate_by = 24
    template_name = 'core/categories.html'
    context_object_name = 'products_list'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            filters = dict(request.GET)
            self.seo = {}
            self.seo['title'] = ''
            self.seo['description'] = ''
            brands = []
            range_sliders = {}
            other_properties = {}
            selected_order = {}
            output_queryset = self.get_queryset()
            if 'brand' in filters:
                split_brands = filters.get('brand')[0].split(',')
                brand = Brand.objects.filter(
                    id__in=split_brands)
                output_queryset = output_queryset.filter(
                    brand__in=split_brands)
                for brand in split_brands:
                    brands.append(brand)
                del filters['brand']
            if 'page' in filters:
                del filters['page']
            if 'price' in filters:
                min_price, max_price = filters.get('price')[0].split(':')
                output_queryset = output_queryset.filter(Q(discount_price__range=(
                    min_price, max_price)) | Q(price__range=(min_price, max_price)))
                del filters['price']
            if 'order' in filters:
                possible_orders = {
                    'popularity': output_queryset.annotate(popularity_count=Count('productview')).order_by('-popularity_count'),
                    'rating': output_queryset.annotate(reviews_avg=Avg('productreview__customer_review')).order_by('reviews_avg'),
                    'published': output_queryset.order_by('-published'),
                    'price_low_to_high': output_queryset.order_by(Coalesce('discount_price', 'price').asc()),
                    'price_high_to_low': output_queryset.order_by(Coalesce('discount_price', 'price').desc()),
                }
                possible_orders_names = {
                    'popularity': 'Популярные',
                    'rating': 'По рейтингу',
                    'published': 'Новинки',
                    'price_low_to_high': 'Подешевле',
                    'price_high_to_low': 'Подороже',
                }
                
                chosen_order = filters.get('order')[0]
                output_queryset = possible_orders.get(
                    chosen_order, '').order_by('not_in_stock')
                selected_order['name'] = possible_orders_names.get(
                    filters.get('order')[0])
                selected_order['is_chosen'] = True
                del filters['order']
            else:
                output_queryset.annotate(popularity_count=Count(
                    'productview')).order_by('-popularity_count'),

            filters_slugs = {}
            for key, values in filters.items():
                try:
                    filters_slugs[key] = PropertyValue.objects.filter(
                        id__in=values[0].split(',')).values_list('slug')
                except ValueError:
                    filters_slugs[key] = values

            for key, value in filters_slugs.items():
                if key.startswith('range'):
                    slug = key[6:]
                    property_min_value, property_max_value = value[0].split(
                        ':')
                    output_queryset = output_queryset.filter(propertyvalue__slug__startswith=slug, propertyvalue__int_value_of_value__range=(
                        property_min_value, property_max_value))
                    range_sliders[slug] = {}
                    range_sliders[slug]['data_from'] = property_min_value
                    range_sliders[slug]['data_to'] = property_max_value
                else:
                    other_properties[key] = []
                    values = []
                    for v in value:
                        values.append(v[0])
                    for val in values:
                        other_properties[key].append(val)
                    output_queryset2 = PropertyValue.objects.none()
                    if not output_queryset2:
                        output_queryset2 = output_queryset.filter(
                            propertyvalue__slug__in=values)
                    else:
                        output_queryset2 |= output_queryset.filter(
                            propertyvalue__slug__in=values)
                    output_queryset = output_queryset2

            paginator = Paginator(output_queryset, 24)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            empty_response = False

            if not page_obj:
                empty_response = True

            context = {
                'products_list': page_obj,
                'page_obj': page_obj,
                'filters': self.get_filter_parameters(output_queryset, range_sliders=range_sliders, other_properties=other_properties, brands=brands),
                'parameters': dict(request.GET),
                'page_url': reverse('core:category-view', kwargs={
                    'slug': self.get_category().slug
                }),
                'seo': self.get_seo_data(other_properties=other_properties, brands=brands, category=self.category),
                'empty_response': True if empty_response else False,
                'selected_order': selected_order,
            }

            return render(request, 'common/category_content.html', context=context)
        else:
            if request.GET:
                filters = dict(request.GET)
                self.seo = {}
                self.seo['title'] = ''
                self.seo['description'] = ''
                brands = []
                range_sliders = {}
                other_properties = {}
                selected_order = {}
                output_queryset = self.get_queryset().order_by('not_in_stock')
                if 'brand' in filters:
                    split_brands = filters.get('brand')[0].split(',')
                    brand = Brand.objects.filter(
                        id__in=split_brands)
                    output_queryset = output_queryset.filter(
                        brand__in=split_brands)
                    for brand in split_brands:
                        brands.append(brand)
                    del filters['brand']
                if 'page' in filters:
                    del filters['page']
                if 'price' in filters:
                    min_price, max_price = filters.get('price')[0].split(':')
                    output_queryset = output_queryset.filter(Q(discount_price__range=(
                        min_price, max_price)) | Q(price__range=(min_price, max_price)))
                    range_sliders['price'] = {}
                    range_sliders['price']['data_from'] = min_price
                    range_sliders['price']['data_to'] = max_price
                    del filters['price']
                if 'order' in filters:
                    possible_orders = {
                        'popularity': output_queryset.annotate(popularity_count=Count('productview')).order_by('-popularity_count'),
                        'rating': output_queryset.annotate(reviews_avg=Avg('productreview__customer_review')).order_by('reviews_avg'),
                        'published': output_queryset.order_by('-published'),
                        'price_low_to_high': output_queryset.order_by(Coalesce('discount_price', 'price').asc()),
                        'price_high_to_low': output_queryset.order_by(Coalesce('discount_price', 'price').desc()),
                    }
                    possible_orders_names = {
                        'popularity': 'Популярные',
                        'rating': 'По рейтингу',
                        'published': 'Новинки',
                        'price_low_to_high': 'Подешевле',
                        'price_high_to_low': 'Подороже',
                    }
                    chosen_order = filters.get('order')[0]
                    output_queryset = possible_orders.get(
                        chosen_order, '').order_by('not_in_stock')
                    selected_order['name'] = possible_orders_names.get(
                        filters.get('order')[0])
                    selected_order['is_chosen'] = True
                    del filters['order']
                else:
                    output_queryset.annotate(popularity_count=Count(
                        'productview')).order_by('-popularity_count'),

                filters_slugs = {}
                for key, values in filters.items():
                    try:
                        filters_slugs[key] = PropertyValue.objects.filter(
                            id__in=values[0].split(',')).values_list('slug')
                    except ValueError:
                        filters_slugs[key] = values

                for key, value in filters_slugs.items():
                    if key.startswith('range'):
                        slug = key[6:]
                        property_min_value, property_max_value = value[0].split(
                            ':')
                        output_queryset = output_queryset.filter(propertyvalue__slug__startswith=slug, propertyvalue__int_value_of_value__range=(
                            property_min_value, property_max_value))
                        range_sliders[slug] = {}
                        range_sliders[slug]['data_from'] = property_min_value
                        range_sliders[slug]['data_to'] = property_max_value
                    else:
                        other_properties[key] = []
                        values = []
                        for v in value:
                            values.append(v[0])
                        for val in values:
                            other_properties[key].append(val)
                        output_queryset2 = PropertyValue.objects.none()
                        if not output_queryset2:
                            output_queryset2 = output_queryset.filter(
                                propertyvalue__slug__in=values)
                        else:
                            output_queryset2 |= output_queryset.filter(
                                propertyvalue__slug__in=values)
                        output_queryset = output_queryset2

                paginator = Paginator(output_queryset, 24)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                empty_response = False

                if not page_obj:
                    empty_response = True
                context = {
                    'main_categories': super().get_main_categories(),
                    'newest_products': super().get_newest_products(),
                    'popular_products': super().get_popular_products(),
                    'order_products': super().get_cart_products(),
                    'products_list': page_obj,
                    'page_obj': page_obj,
                    'filters': self.get_filter_parameters(output_queryset, range_sliders=range_sliders, other_properties=other_properties, brands=brands),
                    'parameters': dict(request.GET),
                    'page_url': reverse('core:category-view', kwargs={
                        'slug': self.get_category().slug
                    }),
                    'seo': self.get_seo_data(other_properties=other_properties, brands=brands, category=self.category),
                    'empty_response': True if empty_response else False,
                    'selected_order': selected_order,
                }

                return render(request, self.template_name, context=context)
            else:
                return super().get(request)

    def get_queryset(self, *args, **kwargs):
        return Product.objects.select_related('category').filter(category__slug=self.kwargs['slug']).annotate(popularity_count=Count('productview')).order_by('not_in_stock', '-popularity_count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_categories'] = super().get_main_categories()
        context['newest_products'] = super().get_newest_products()
        context['popular_products'] = super().get_popular_products()
        context['order_products'] = super().get_cart_products()
        context['filters'] = self.get_filter_parameters(self.get_queryset())
        context['page_url'] = reverse(
            'core:category-view', kwargs={'slug': self.get_category().slug})
        context['empty_response'] = False
        context['order'] = {'name': 'Популярные'}
        return context

    def get_filter_parameters(self, queryset, **kwargs):
        category = self.get_category()
        self.category = category
        # properties = Property.objects.prefetch_related('propertyvalue_set').prefetch_related('propertyvalue_set__product').prefetch_related('propertyvalue_set__product__category').filter(
        #     categories=category).annotate(min_value=Min('propertyvalue__int_value_of_value', filter=Q(propertyvalue__product__category=category)), max_value=Max('propertyvalue__int_value_of_value', filter=Q(propertyvalue__product__category=category)),)

        brands = []
        properties = {}
        range_sliders = {}
        other_properties = {}
        if kwargs:
            if 'range_sliders' in kwargs:
                range_sliders = kwargs.get('range_sliders')
            if 'other_properties' in kwargs:
                other_properties = kwargs.get('other_properties')
            if 'brands' in kwargs:
                brands = kwargs.get('brands')

        output_brands = Brand.objects.filter(category=category).values()
        for brand in output_brands:
            if str(brand['id']) in brands:
                brand['checked'] = True

        for product in queryset.prefetch_related('propertyvalue_set').prefetch_related('propertyvalue_set__property').select_related('brand'):
            for property_value in product.propertyvalue_set.all():
                if property_value.property.slug not in properties:
                    properties[property_value.property.slug] = {}
                    properties[property_value.property.slug]['name'] = property_value.property.name
                    properties[property_value.property.slug]['weight'] = property_value.property.weight
                    properties[property_value.property.slug]['slug'] = property_value.property.slug
                    properties[property_value.property.slug]['dynamic_seo'] = property_value.property.dynamic_seo
                    properties[property_value.property.slug]['property_values'] = {}

                if property_value.slug not in properties[property_value.property.slug]['property_values']:
                    properties[property_value.property.slug]['property_values'][property_value.slug] = {
                    }
                    properties[property_value.property.slug]['property_values'][property_value.slug]['id'] = property_value.id
                    properties[property_value.property.slug]['property_values'][property_value.slug]['value'] = property_value.value
                    properties[property_value.property.slug]['property_values'][property_value.slug]['slug'] = property_value.slug
                    properties[property_value.property.slug]['property_values'][
                        property_value.slug]['int_value_of_value'] = property_value.int_value_of_value

                    if properties[property_value.property.slug]['slug'] in other_properties:
                        properties[property_value.property.slug]['expanded'] = True
                        if properties[property_value.property.slug]['property_values'][property_value.slug]['slug'] in other_properties.get(properties[property_value.property.slug]['slug']):
                            properties[property_value.property.slug]['property_values'][property_value.slug]['checked'] = True

                    if property_value.property.range_slider and property_value.int_value_of_value:
                        properties[property_value.property.slug]['range_slider'] = True

                        if 'min_value' not in properties[property_value.property.slug] and 'max_value' not in properties[property_value.property.slug]:
                            properties_from_database = Property.objects.filter(
                                slug=property_value.property.slug, categories=category)
                            properties[property_value.property.slug]['min_value'] = properties_from_database.aggregate(
                                Min('propertyvalue__int_value_of_value')).get('propertyvalue__int_value_of_value__min')
                            properties[property_value.property.slug]['max_value'] = properties_from_database.aggregate(
                                Max('propertyvalue__int_value_of_value')).get('propertyvalue__int_value_of_value__max')
                            if range_sliders:
                                if properties[property_value.property.slug]['slug'] in range_sliders:
                                    properties[property_value.property.slug]['flag'] = True
                                    properties[property_value.property.slug]['data_from'] = range_sliders.get(
                                        properties[property_value.property.slug]['slug'])['data_from']
                                    properties[property_value.property.slug]['data_to'] = range_sliders.get(
                                        properties[property_value.property.slug]['slug'])['data_to']

                    else:
                        properties[property_value.property.slug]['range_slider'] = False
                else:
                    continue

        for key, property in properties.items():
            if property['range_slider'] is False:
                property['property_values'] = sorted(
                    property['property_values'].items(), key=lambda x: x[1]['int_value_of_value'] if x[1]['int_value_of_value'] is not None else 0, reverse=False)

        properties = dict(
            sorted(properties.items(), key=lambda x: x[1]['weight']))

        queryset_products_min_discount_price = queryset.aggregate(
            Min('discount_price')).get('discount_price__min')
        queryset_products_min_price = queryset.aggregate(
            Min('price')).get('price__min')

        output_price = {}
        if queryset_products_min_discount_price and queryset_products_min_price:
            output_price['min_price'] = queryset_products_min_discount_price if queryset_products_min_discount_price < queryset_products_min_price else queryset_products_min_price
        elif queryset_products_min_discount_price:
            output_price['min_price'] = queryset_products_min_discount_price
        elif queryset_products_min_price:
            output_price['min_price'] = queryset_products_min_price
        else:
            output_price['min_price'] = 0

        queryset_products_max_discount_price = queryset.aggregate(
            Max('discount_price')).get('discount_price__max')
        queryset_products_max_price = queryset.aggregate(
            Max('price')).get('price__max')

        if queryset_products_max_discount_price and queryset_products_max_price:
            output_price['max_price'] = queryset_products_max_discount_price if queryset_products_max_discount_price < queryset_products_max_price else queryset_products_max_price
        elif queryset_products_max_discount_price:
            output_price['max_price'] = queryset_products_max_discount_price
        elif queryset_products_max_price:
            output_price['max_price'] = queryset_products_max_price
        else:
            output_price['max_price'] = 0

        if 'price' in range_sliders:
            output_price['data_from'] = int(
                range_sliders.get('price')['data_from'])
            output_price['data_to'] = int(
                range_sliders.get('price')['data_to'])
        return {
            'brands': output_brands,
            'parent_category': category,
            'properties': properties,
            'output_price': output_price,
        }

    def get_seo_data(self, *args, **kwargs):
        seo = {}
        seo['title'] = ''
        seo['description'] = ''
        if kwargs:
            if 'other_properties' in kwargs:
                other_properties = kwargs.get('other_properties')
            if 'brands' in kwargs:
                brands = list(Brand.objects.filter(
                    id__in=kwargs.get('brands')).values_list('name'))
            properties = Property.objects.none()
            for key, value in other_properties.items():
                properties |= Property.objects.filter(slug=key)

            for brand in brands:
                seo['title'] = f"{'' if seo['title'] == '' else seo['title'] + ', '}{''.join(map(str, brand))}"
                seo[
                    'description'] = f"{'' if seo['description'] == '' else seo['description'] + ', '}{''.join(map(str, brand))}"

            if seo['title'] != '':
                seo['description'] += '; '

            seo_data_has_properties_with_dynamic_seo = False
            for property in properties:
                if property.dynamic_seo:
                    seo_data_has_properties_with_dynamic_seo = True
                    seo[
                        'description'] = f"{seo['description']}{property.name}: {', '.join(other_properties[property.slug])}; "

            if not seo_data_has_properties_with_dynamic_seo:
                seo['description'] = seo['description'][:-2]

            if self.category:
                if seo['title'] and self.category.where_to_insert_dynamic_page_title_data:
                    page_title = self.category.page_title.split(' ')
                    page_title.insert(
                        self.category.where_to_insert_dynamic_page_title_data, seo['title'])
                    seo['title'] = ' '.join(page_title)

                if seo['description'] and self.category.where_to_insert_dynamic_meta_description_data:
                    meta_description = self.category.meta_description.split(
                        ' ')
                    meta_description.insert(
                        self.category.where_to_insert_dynamic_meta_description_data, seo['description'])
                    seo['description'] = ' '.join(meta_description)

        return seo

    def get_category(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        if bool(category) is True:
            return category
        else:
            raise Http404


class OrderSummaryView(View, BasePage):
    def get(self, *args, **kwargs):
        try:
            if self.request.user.is_authenticated:
                basket = Basket.objects.filter(
                    user=self.request.user, is_ordered=False).prefetch_related('products')[0]
            else:
                basket = Basket.objects.filter(
                    pk=self.request.session.get('cart_id', None), is_ordered=False).prefetch_related('products')[0]

            total_sum = 0
            for product in basket.products.all():
                total_sum += product.get_total_summary()

            context = {
                'object': basket,
                'total_sum': total_sum,
                'newest_products': super().get_newest_products(),
                'popular_products': super().get_popular_products(),
                'main_categories': super().get_main_categories(),
                'order_products': super().get_cart_products(),
                'seo': super().get_seo(self.request)
            }
        except IndexError:
            messages.error(
                self.request, 'У вас нет активной корзины. Добавьте товар.')
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        except ObjectDoesNotExist:
            messages.error(
                self.request, 'У вас нет активной корзины. Добавьте товар.')
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
        return render(self.request, 'core/cart.html', context)


class ProductDetailView(DetailView, BasePage):
    model = Product
    template_name = 'core/single-product.html'

    def get(self, request, *args, **kwargs):
        # Adding or not views count of current product
        self.record_product_view()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.model.objects.filter(slug=self.kwargs.get('slug')).prefetch_related(
            'propertyvalue_set').prefetch_related('propertyvalue_set__property').prefetch_related('category__extraoption_set')
        return queryset.prefetch_related('productreview_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        instance = self.get_object()
        if len(instance.productreview_set.all()) > 0:
            # product_review_avg = round(instance.productreview_set.filter(published=True).aggregate(
            #    Avg('customer_review')).get('customer_review__avg'), 2)
            product_review_avg = instance.productreview_set.filter(
                published=True)
            product_review_avg = product_review_avg.aggregate(
                Avg('customer_review'))
            product_review_avg = product_review_avg.get('customer_review__avg')
            product_review_avg = round(
                product_review_avg, 2) if product_review_avg else None
        else:
            product_review_avg = 0
        instance_images = list(instance.productimage_set.all())
        reviews_list = instance.productreview_set.filter(published=True).values(
            'customer_review').annotate(count=Count('customer_review')).order_by('-customer_review')

        total_reviews_count = 0
        for review in reviews_list:
            total_reviews_count += review['count']

        context['total_reviews_count'] = total_reviews_count
        context['reviews_list'] = reviews_list
        context['product_images'] = instance_images
        context['main_categories'] = super().get_main_categories()
        context['product_review_avg'] = product_review_avg
        context['newest_products'] = super().get_newest_products()
        context['popular_products'] = super().get_popular_products()
        context['order_products'] = super().get_cart_products()
        context['product_property_values'] = self.get_product_property_value()
        context['product_reviews'] = self.get_product_published_reviews()
        context['delievery_options'] = DelieveryOption.objects.all()
        return context

    def record_product_view(self):
        slug = self.kwargs.get('slug')
        product = get_object_or_404(Product, slug=slug)
        user_already_visited_page = ProductView.objects.filter(
            product=product, ip=self.request.META['REMOTE_ADDR'])
        if not user_already_visited_page:
            view = ProductView(
                product=product, ip=self.request.META['REMOTE_ADDR'])
            view.save()
        product.views_count = ProductView.objects.filter(
            product=product).count()
        product.save()

    def get_product_property_value(self):
        return self.get_queryset()[0].propertyvalue_set.all().order_by('property__weight', 'property__id')

    def get_product_published_reviews(self):
        return self.get_queryset()[0].productreview_set.filter(published=True)


class CheckoutView(View, BasePage):
    def get(self, *args, **kwargs):
        logged_as_user, anonymous_user_has_cart = self.request.user.is_authenticated, self.request.session.get(
            'has_cart', None) == '1'
        if logged_as_user or anonymous_user_has_cart:
            if logged_as_user:
                basket = Basket.objects.filter(
                    user=self.request.user, is_ordered=False).prefetch_related('products').prefetch_related('products__product').prefetch_related('products__product__category').first()
            elif anonymous_user_has_cart:
                basket = Basket.objects.filter(pk=self.request.session.get(
                    'cart_id', None), is_ordered=False).prefetch_related('products').prefetch_related('products__product').prefetch_related('products__product__category').first()
            else:
                messages.error(self.request, 'Ваша корзина пуста.')
                return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

            if basket:
                order_products = basket.products.all()
                delievery_cost = 0
                for order_product in order_products:
                    if order_product.product.category.count_delievery_cost_for_each_product:
                        delievery_cost += order_product.product.category.delievery_cost * order_product.quantity

                if delievery_cost < 100:
                    delievery_cost = 100

                user_billing_address = None
                if logged_as_user:
                    user_billing_address = self.request.user.billingaddress_set.first()
                if user_billing_address:
                    form = CheckoutForm(initial={
                        'customer_first_name': user_billing_address.customer_first_name,
                        'last_name': user_billing_address.last_name,
                        'street_address': user_billing_address.street_address,
                        'city_address': user_billing_address.city_address,
                        'postcode': user_billing_address.postcode,
                        'email': user_billing_address.email,
                        'phone': user_billing_address.phone,
                        'delievery_option': user_billing_address.delievery_option,
                        'payment_option': user_billing_address.payment_option,
                    })
                else:
                    form = CheckoutForm()
                delievery_options = DelieveryOption.objects.all()
                payment_options = PaymentOption.objects.all()

                context = {
                    'form': form,
                    'delievery_options': delievery_options,
                    'payment_options': payment_options,
                    'basket': basket,
                    'delievery_cost': delievery_cost,
                    'newest_products': super().get_newest_products(),
                    'popular_products': super().get_popular_products(),
                    'main_categories': super().get_main_categories(),
                    'order_products': super().get_cart_products(),
                    'seo': super().get_seo(self.request)

                }
                return render(self.request, 'core/checkout.html', context)
            else:
                messages.error(self.request, 'Ваша корзина пуста')
                return redirect('core:home')
        else:
            messages.error(self.request, 'Ваша корзина пуста.')
            return redirect('core:home')

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if self.request.user.is_authenticated:
            basket = Basket.objects.get(
                user=self.request.user, is_ordered=False)
        elif self.request.session.get('has_cart', None) == '1' and self.request.session.get('cart_id', None) is not None:
            basket = Basket.objects.get(pk=self.request.session.get(
                'cart_id', None), is_ordered=False)
        else:
            raise ObjectDoesNotExist()
        if form.is_valid():
            customer_first_name = form.cleaned_data.get('customer_first_name')
            last_name = form.cleaned_data.get('last_name')
            street_address = form.cleaned_data.get('street_address')
            city_address = form.cleaned_data.get('city_address')
            postcode = form.cleaned_data.get('postcode')
            email = form.cleaned_data.get('email')
            phone = str(form.cleaned_data.get('phone'))
            create_an_account = form.cleaned_data.get('create_an_account')
            sign_in_password = form.cleaned_data.get('sign_in_password')
            payment = form.cleaned_data.get('payment')
            terms_and_conditions = form.cleaned_data.get(
                'terms_and_conditions')
            try:
                delievery_option = DelieveryOption.objects.get(
                    id=self.request.POST.get('delievery'))
                payment_option = PaymentOption.objects.get(
                    slug=self.request.POST.get('payment'))
            except ObjectDoesNotExist:
                messages.error(
                    self.request, 'Пожалуйста заполните способ доставки и способ оплаты!')
                return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

            credit_option = self.request.POST.get('credit')
            total_summary = cart_total_summary(self.request)
            account_created = False
            user_created = False
            if create_an_account:
                try:
                    user_created = User.objects.create_user(
                        username=email,
                        first_name=customer_first_name,
                        last_name=last_name,
                        email=email,
                        password=sign_in_password,
                    )
                except Exception as e:
                    messages(
                        self.request, 'Непредвиденная ошибка, обратитесь за помощью к администратору: help@tehnomall.md')
                    return redirect(self.request, 'core:home')
                account_created = True
            if account_created is True and user_created is not None:
                billing_address = BillingAddress(
                    user=user_created,
                    customer_first_name=customer_first_name,
                    last_name=last_name,
                    street_address=street_address,
                    city_address=city_address,
                    postcode=postcode,
                    email=email,
                    phone=phone,
                    delievery_option=delievery_option,
                    payment_option=payment_option
                )
                billing_address.save()
                basket.billing_address = billing_address
                basket.save()
                time = timezone.now()

                if delievery_option.id == 1:
                    order_products = basket.products.all()
                    delievery_cost = 0
                    for order_product in order_products:
                        if order_product.product.category.count_delievery_cost_for_each_product:
                            delievery_cost += order_product.product.category.delievery_cost * order_product.quantity

                    if delievery_cost < 100:
                        delievery_cost = 100

                    delievery_payment = delievery_cost
                else:
                    delievery_payment = 0

                if credit_option:
                    customer_wants_credit = True
                    credit_duration = int(credit_option)
                    percent = total_summary / 100
                    additional_percent = 2 * credit_duration
                    summary_with_credit = percent * (100 + additional_percent)
                    credit_month_payment = summary_with_credit / credit_duration
                else:
                    customer_wants_credit = False
                    credit_duration = 0
                    credit_month_payment = 0
                ordered_basket = OrderedBasket.objects.create(
                    user=user_created,
                    basket=basket,
                    billing_address=billing_address,
                    ordered_date=time,
                    total_summary=total_summary,
                    customer_wants_credit=customer_wants_credit,
                    credit_duration=credit_duration,
                    credit_month_payment=credit_month_payment,
                    delievery_payment=delievery_payment,
                )
            else:
                user = self.request.user if self.request.user.is_authenticated else None
                billing_address = BillingAddress(
                    user=user,
                    customer_first_name=customer_first_name,
                    last_name=last_name,
                    street_address=street_address,
                    city_address=city_address,
                    postcode=postcode,
                    email=email,
                    phone=phone,
                    delievery_option=delievery_option,
                    payment_option=payment_option
                )
                billing_address.save()
                basket.billing_address = billing_address
                basket.is_ordered = True
                basket.save()
                time = timezone.now()

                if delievery_option.id == 1:
                    order_products = basket.products.all()
                    delievery_cost = 0
                    for order_product in order_products:
                        if order_product.product.category.count_delievery_cost_for_each_product:
                            delievery_cost += order_product.product.category.delievery_cost * order_product.quantity

                    if delievery_cost < 100:
                        delievery_cost = 100

                    delievery_payment = delievery_cost
                else:
                    delievery_payment = 0

                if credit_option:
                    customer_wants_credit = True
                    credit_duration = int(credit_option)
                    percent = total_summary / 100
                    additional_percent = 2 * credit_duration
                    summary_with_credit = percent * (100 + additional_percent)
                    credit_month_payment = summary_with_credit / credit_duration
                else:
                    customer_wants_credit = False
                    credit_duration = 0
                    credit_month_payment = 0
                ordered_basket = OrderedBasket.objects.create(
                    user=user,
                    basket=basket,
                    billing_address=billing_address,
                    ordered_date=time,
                    total_summary=total_summary,
                    customer_wants_credit=customer_wants_credit,
                    credit_duration=credit_duration,
                    credit_month_payment=credit_month_payment,
                    delievery_payment=delievery_payment,
                )
            return redirect('core:home')
        return redirect('core:checkout')


class ContactsPageView(View, BasePage):
    template_name = 'core/contacts.html'

    def get(self, request):

        form = LeaveTheMessageForm()

        context = {
            'form': form,
            'main_categories': super().get_main_categories(),
            'newest_products': super().get_newest_products(),
            'popular_products': super().get_popular_products(),
            'order_products': super().get_cart_products(),
            'seo': super().get_seo(request),

        }
        return render(request, self.template_name, context)

    def post(self, request):
        try:
            form = LeaveTheMessageForm(self.request.POST or None)
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('email')
                subject = form.cleaned_data.get('subject')
                message = form.cleaned_data.get('message')
                recipient_list = ['help@tehnomall.md']
                if first_name and email and message:
                    html_message = render_to_string('forms/from_contacts_page.html', {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'subject': subject,
                        'message': message,
                    })
                    plain_message = strip_tags(html_message)
                    email_from = recipient_list[0]
                    try:
                        send_mail(
                            f"Вам пришло письмо со страницы 'Контакты' от {first_name}",
                            plain_message,
                            email_from,
                            recipient_list,
                            html_message=html_message
                        )
                    except BadHeaderError:
                        messages.error(
                            request, "Что-то пошло не так с отправкой Вашей формы. Пожалуйста, свяжитесь напрямую с администратором: help@tehnomall.md")
        except Exception as e:
            messages.error(
                'Непредвиденная ошибка, обратитесь за помощью к администратору: help@tehnomall.md')
        return redirect('core:contacts')


class FAQPageView(View, BasePage):
    template_name = 'core/faq.html'

    def get(self, request):
        context = {
            'main_categories': super().get_main_categories(),
            'newest_products': super().get_newest_products(),
            'popular_products': super().get_popular_products(),
            'order_products': super().get_cart_products(),
            'seo': super().get_seo(request),

        }
        return render(request, self.template_name, context)


class TermsAndConditionsPageView(View, BasePage):
    template_name = 'core/terms-and-conditions.html'

    def get(self, request, *args, **kwargs):
        context = {
            'main_categories': super().get_main_categories(),
            'newest_products': super().get_newest_products(),
            'popular_products': super().get_popular_products(),
            'order_products': super().get_cart_products(),
            'seo': super().get_seo(request),
        }
        return render(request, self.template_name, context)


class CreditPageView(View, BasePage):
    template_name = 'core/credit.html'

    def get(self, request, *args, **kwargs):
        context = {
            'main_categories': super().get_main_categories(),
            'newest_products': super().get_newest_products(),
            'popular_products': super().get_popular_products(),
            'order_products': super().get_cart_products(),
            'seo': super().get_seo(request),
        }
        return render(request, self.template_name, context)


def add_to_cart(request, slug,):
    extra_options = request.POST.getlist('extra-option')
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        product_count = int(request.POST['product_total_count'])
    else:
        product_count = 1
    if request.user.is_authenticated:
        order_product, created = BasketProduct.objects.get_or_create(
            product=product,
            user=request.user,
            is_ordered=False)
        order_qs = Basket.objects.filter(user=request.user, is_ordered=False)
        if order_qs.exists():
            basket = order_qs[0]
            if basket.products.filter(product__slug=product.slug).exists():
                order_product.quantity += product_count
                order_product.save()
                messages.info(
                    request, 'Кол-во данного товара было успешно увеличено')
            else:
                messages.info(
                    request, 'Данный товар был успешно добавлен в Вашу корзину')
                order_product.quantity = product_count
                order_product.save()
                basket.products.add(order_product)
        else:
            ordered_date = timezone.now()
            basket = Basket.objects.create(
                user=request.user, ordered_date=ordered_date)
            order_product.quantity = product_count
            order_product.save()
            basket.products.add(order_product)
            messages.info(
                request, 'Данный товар был успешно добавлен в Вашу корзину')
            basket.products.add(order_product)
    else:
        if request.session.get('has_cart', None) == '1':
            order_qs = Basket.objects.filter(
                pk=request.session['cart_id'], is_ordered=False)
            if order_qs.exists():
                basket = order_qs[0]
                order_product, created = BasketProduct.objects.get_or_create(
                    product=product,
                    basket=basket,
                    is_ordered=False)
                if basket.products.filter(product__slug=product.slug).exists():
                    order_product.quantity += product_count
                    order_product.save()
                    messages.info(
                        request, 'Кол-во данного товара было успешно увеличено')
                else:
                    messages.info(
                        request, 'Данный товар был успешно добавлен в Вашу корзину')
                    order_product.quantity = product_count
                    order_product.save()
                    basket.products.add(order_product)

            else:
                ordered_date = timezone.now()
                basket = Basket.objects.create(ordered_date=ordered_date)
                order_product, created = BasketProduct.objects.get_or_create(
                    product=product,
                    basket=basket,
                    is_ordered=False)
                order_product.quantity = product_count
                order_product.save()
                basket.products.add(order_product)
                request.session['cart_id'] = basket.pk
                messages.info(
                    request, 'Данный товар был успешно добавлен в Вашу корзину')
        else:
            ordered_date = timezone.now()
            basket = Basket.objects.create(ordered_date=ordered_date)
            order_product, created = BasketProduct.objects.get_or_create(
                product=product,
                basket=basket,
                is_ordered=False)
            order_product.quantity = product_count
            order_product.save()
            basket.products.add(order_product)
            request.session['has_cart'] = '1'
            request.session['cart_id'] = basket.pk
            messages.info(
                request, 'Данный товар был успешно добавлен в Вашу корзину')
    if extra_options:
        try:
            extra_options_from_database = ExtraOption.objects.filter(
                id__in=extra_options)
            for extra_option in extra_options_from_database:
                extra_option_ordered, created = ExtraOptionOrdered.objects.get_or_create(
                    name=extra_option.name,
                    cost=extra_option.cost,
                    slug=extra_option.slug,
                    option=extra_option,
                    basket_product=order_product,
                )
                if not created:
                    extra_option_ordered.count += product_count
                else:
                    extra_option_ordered.count = product_count
                extra_option_ordered.save()
        except Exception:
            messages.info(
                request, "Что-то пошло не так, пожалуйста, свяжитесь с администратором")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.user.is_authenticated:
        order_qs = Basket.objects.filter(user=request.user, is_ordered=False)
        if order_qs.exists():
            basket = order_qs[0]
            if basket.products.filter(product__slug=product.slug).exists():
                order_product = BasketProduct.objects.filter(
                    product=product,
                    user=request.user,
                    is_ordered=False)[0]
                basket.products.remove(order_product)
                order_product.delete()
                messages.info(
                    request, 'Данный товар был успешно удален из Вашей корзины')
            else:
                messages.info(request, 'Данного товара нет в вашей корзине.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(
                request, 'У вас нет активной корзины. Добавьте товар.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        if request.session.get('has_cart', None) == '1':
            order_qs = Basket.objects.filter(
                pk=request.session['cart_id'], is_ordered=False)
            if order_qs.exists():
                basket = order_qs[0]
                if basket.products.filter(product__slug=product.slug).exists():
                    order_product, created = BasketProduct.objects.get_or_create(
                        product=product,
                        basket=basket,
                        is_ordered=False)
                    basket.products.remove(order_product)
                    order_product.delete()
                    messages.info(
                        request, 'Данный товар был успешно удален из Вашей корзины')
                else:
                    messages.info(
                        request, 'Данного товара нет в вашей корзине.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.info(
                    request, 'У вас нет активной корзины. Добавьте товар.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.info(
                request, 'У вас нет активной корзины. Добавьте товар.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_cart(request):

    if request.user.is_authenticated:
        basket = Basket.objects.filter(
            user=request.user, is_ordered=False).prefetch_related('products')[0]
    else:
        basket = Basket.objects.filter(
            pk=request.session.get('cart_id', None), is_ordered=False).prefetch_related('products')[0]
    for data_form in request.POST:
        if data_form == 'csrfmiddlewaretoken':
            continue
        if data_form.startswith('extra-option-'):
            extra_option = product.extraoptionordered_set.filter(
                slug=data_form[13:])[0]
            extra_option.count = int(request.POST[data_form])
            extra_option.save()
            basket.products.update()
            continue
        product = basket.products.filter(product__slug=data_form)[
            0]
        product.quantity = int(request.POST[data_form])
        product.save()
        basket.products.update()

    if request.is_ajax():
        return render(request, 'common/cart_products_table.html', {'object': basket})
    else:
        return redirect('core:basket-summary')


def leave_product_review(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if len(request.POST) > 1:
        user_already_left_the_comment_to_current_product = ProductReview.objects.filter(
            product=product, customer_ip=request.META['REMOTE_ADDR'], customer_session=request.session.session_key) or ProductReview.objects.filter(product=product, customer=request.user)
        if not user_already_left_the_comment_to_current_product:
            post = request.POST
            customer_name = str(post['name'])
            customer_email = str(post['email'])
            customer_review = float(post['review']) if float(
                post['review']) < 5.0 and float(post['review']) >= 0.0 else 5.0
            customer_review_text = str(post['review_text'])
            product.productreview_set.create(
                customer=request.user, customer_ip=request.META['REMOTE_ADDR'], customer_name=customer_name, customer_session=request.session.session_key, customer_email=customer_email, customer_review=customer_review, customer_review_text=customer_review_text).save()
            published = False
        else:
            messages.error(
                request, 'Вы уже оставили комментарий к данному продукту')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_to_compare(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
    except Exception as e:
        messages.error(
            request, 'Возникла непредвиденная ошибка, пожалуйста свяжитесь с тех. поддержкой - help@tehnomall.md')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    session = request.session['compare'] if request.session.get(
        'compare', None) else None

    if session:
        if len(session) > 5:
            messages.warning(
                request, 'Максимально допустимое количество товаров: 5')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if product.id not in session:
            session.append(product.id)
            request.session['compare'] = session
            messages.success(request, 'Товар добавлен в Ваш список сравнений')
        else:
            messages.warning(
                request, 'Этот товар уже добавлен в Ваш список сравнений')
    else:
        session = [product.id]
        request.session['compare'] = session
        messages.success(
            request, 'Список сравнений был успешно создан. Товар добавлен в Ваш список сравнений.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_compare(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
    except Exception as e:
        messages.error(
            request, 'Возникла непредвиденная ошибка, пожалуйста свяжитесь с тех. поддержкой - help@tehnomall.md')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    session = request.session['compare'] if request.session.get(
        'compare', None) else None
    if session:
        if product.id in session:
            session.remove(product.id)
            request.session['compare'] = session
        else:
            messages.warning(
                request, 'Данного товара нет в Вашем списке товаров для сравнения')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'У Вас нет списка товаров для сравнения')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ComparePageView(View, BasePage):

    def get(self, request, *args, **kwargs):

        try:
            products = Product.objects.filter(
                id__in=request.session['compare']).prefetch_related('propertyvalue_set').prefetch_related('productreview_set').prefetch_related('propertyvalue_set__property')
        except Exception as e:

            return render(request, 'core/compare.html')

        products = products.annotate(Avg('productreview__customer_review'))

        table = {}
        for product in products:
            for pv in product.propertyvalue_set.all():
                if table.get(pv.property.id) is None:
                    table[pv.property.id] = {}
                    table[pv.property.id]['name'] = pv.property.name
                    table[pv.property.id]['products'] = {}
                table[pv.property.id]['products'][product.id] = pv.value

        context = {
            'main_categories': super().get_main_categories(),
            'newest_products': super().get_newest_products(),
            'popular_products': super().get_popular_products(),
            'order_products': super().get_cart_products(),
            'seo': super().get_seo(request),
            'products': products,
            'table': table,
        }

        return render(request, 'core/compare.html', context)


def add_to_wishlist(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
    except Exception as e:
        messages.error(
            request, 'Возникла непредвиденная ошибка, пожалуйста свяжитесь с тех. поддержкой - help@tehnomall.md')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    session = request.session['wishlist'] if request.session.get(
        'wishlist', None) else None

    if session:
        if len(session) > 50:
            messages.warning(
                request, 'Максимально допустимое количество товаров: 50')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if product.id not in session:
            session.append(product.id)
            request.session['wishlist'] = session
            messages.success(request, 'Товар добавлен в Ваши избранные')
        else:
            messages.warning(
                request, 'Этот товар уже добавлен в Ваши избранные')
    else:
        session = [product.id]
        request.session['wishlist'] = session
        messages.success(
            request, 'Список избранных товаров был успешно создан. Товар добавлен в Ваши избранные.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_from_wishlist(request, slug):
    try:
        product = get_object_or_404(Product, slug=slug)
    except Exception as e:
        messages.error(
            request, 'Возникла непредвиденная ошибка, пожалуйста свяжитесь с тех. поддержкой - help@tehnomall.md')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    session = request.session['wishlist'] if request.session.get(
        'wishlist', None) else None
    if session:
        if product.id in session:
            session.remove(product.id)
            request.session['wishlist'] = session
        else:
            messages.warning(
                request, 'Данного товара нет в Ваших избранных')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'У Вас нет избранных товаров')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class WishlistPageView(View, BasePage):
    def get(self, request, *args, **kwargs):
        try:
            products = Product.objects.filter(
                id__in=request.session['wishlist'])
        except KeyError:
            return render(request, 'core/wishlist.html')

        context = {
            'main_categories': super().get_main_categories(),
            'newest_products': super().get_newest_products(),
            'popular_products': super().get_popular_products(),
            'order_products': super().get_cart_products(),
            'seo': super().get_seo(request),
            'products': products,
        }

        return render(request, 'core/wishlist.html', context)


class Search(ListView, BasePage):
    model = Product
    template_name = 'core/search-result.html'
    context_object_name = 'products_list'
    paginate_by = 16

    def get(self, request):
        if len(request.GET) > 1:
            output_queryset = self.get_queryset()
            filters = dict(self.request.GET)
            selected_order = {}
            if 'order' in filters:
                possible_orders = {
                    'popularity': output_queryset.annotate(popularity_count=Count('productview')).order_by('-popularity_count'),
                    'rating': output_queryset.annotate(reviews_avg=Avg('productreview__customer_review')).order_by('reviews_avg'),
                    'published': output_queryset.order_by('-published'),
                    'price_low_to_high': output_queryset.order_by(Coalesce('discount_price', 'price').asc()),
                    'price_high_to_low': output_queryset.order_by(Coalesce('discount_price', 'price').desc()),
                }
                possible_orders_names = {
                    'popularity': 'Популярные',
                    'rating': 'По рейтингу',
                    'published': 'Новинки',
                    'price_low_to_high': 'Подешевле',
                    'price_high_to_low': 'Подороже',
                }
                chosen_order = filters.get('order')[0]
                output_queryset = possible_orders.get(
                    chosen_order, '').order_by('not_in_stock')
                selected_order['name'] = possible_orders_names.get(
                    filters.get('order')[0])
                selected_order['is_chosen'] = True
                del filters['order']

            empty_response = False
            if not output_queryset:
                empty_response = True

            paginator = Paginator(output_queryset, 24)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                'products_list': page_obj,
                'page_obj': page_obj,
                'empty_response': True if empty_response else False,
                'selected_order': selected_order,
            }

            return render(request, 'common/search_products_table.html', context=context)
        else:
            return super().get(request)

    def get_queryset(self):
        q = self.request.GET.get('product')
        vector = SearchVector('category__name', 'brand__name',
                              'name', raw=True, fields=('name'))
        vector_trgm = TrigramSimilarity('category__name', q, raw=True, fields=('name')) + TrigramSimilarity(
            'brand__name', q, raw=True, fields=('name')) + TrigramSimilarity('name', q, raw=True, fields=('name'))

        result = self.model.objects.annotate(search=vector).order_by('not_in_stock', 'price').filter(
            search=q) or self.model.objects.annotate(similarity=vector_trgm).filter(similarity__gt=0.2).order_by('price')
        self.empty_response = False
        if not result:
            self.empty_response = True

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_categories'] = super().get_main_categories()
        context['newest_products'] = super().get_newest_products()
        context['popular_products'] = super().get_popular_products()
        context['order_products'] = super().get_cart_products()
        context['seo'] = super().get_seo(self.request)
        context['empty_response'] = self.empty_response
        context['page_url'] = reverse('core:search-product')
        return context


def email(request):

    subject = 'Добро пожаловать в Tehnomall!'
    message = 'Мы рады, что Вы присоединились к команде Tehnomall. Для нас это многое значит. Пожалуйста, не стесняйтесь обращаться за помощью: help@tehnomall.md'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['wishgooddeeds@gmail.com', ]
    send_mail(subject, message, email_from, recipient_list)
    return redirect('core:home')


def get_all_reviews(request, slug):
    if request.is_ajax():
        all_reviews = ProductReview.objects.filter(
            product__slug=slug, published=True)
        context = {
            'all_reviews': all_reviews,
        }
        return render(request, 'common/all_reviews.html', context)
    else:
        messages.error(
            request, 'Возникла непредвиденная ошибка, пожалуйста свяжитесь с тех. поддержкой - help@tehnomall.md')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def leave_customer_phone(request):
    user_already_left_the_phone = CustomerRequestToCallBack.objects.filter(
        ip=request.META['REMOTE_ADDR']) or CustomerRequestToCallBack.objects.filter(customer=request.user)
    if not user_already_left_the_phone or int(user_already_left_the_phone.count()) <= 3:
        post = request.POST
        phone = str(post['phone'])
        name = str(post['name'])
        comment = str(post['comment'])
        CustomerRequestToCallBack.objects.create(
            phone=phone, name=name, comment=comment, customer=request.user, ip=request.META['REMOTE_ADDR'], customer_called_back=False)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=201)


# def percent(number, percent):
#     one_percent_from_given_number = int(number) / 100
#     summary = one_percent_from_given_number * percent
#     result = math.ceil(number - summary)
#     if number > 1000:
#         how_much_to_nine = 10 - (result % 10)
#         result = result + (how_much_to_nine - 1)
#     return result


# # def percent_to_reduce():

#     for p in products:
#         if p.discount_price:
#             p.discount_price = percent(p.discount_price, 2)
#         else:
#             p.price = percent(p.price, 2)
#         p.save()
