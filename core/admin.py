from django.contrib import admin
from django.http import JsonResponse
from mptt.admin import DraggableMPTTAdmin

from .models import (
    MoneyRate,
    BillingAddress,
    Category,
    CustomerRequestToCallBack,
    DelieveryOption,
    DelieveryCityOption,
    ExtraOption,
    Product,
    BasketProduct,
    Basket,
    HomePageBannerImage,
    HotProduct,
    Page,
    PaymentOption,
    Property,
    PropertyValue,
    Brand,
    ProductImage,
    ProductView,
    ProductReview,
    OrderedBasket,
)


class PropertyValueInline(admin.TabularInline):
    model = PropertyValue
    extra = 1
    fields = ('property', 'value',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.is_ajax():
            if db_field.name == 'property':
                kwargs["queryset"] = Property.objects.filter(
                    categories=request.GET.get('category'))
                return super().formfield_for_foreignkey(db_field, request, **kwargs)

        else:
            if db_field.name == "property":
                if request.GET.get('category'):
                    kwargs["queryset"] = Property.objects.all()
                return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PropertyValueAdmin(admin.ModelAdmin):
    autocomplete_fields = ['property']
    search_fields = ['value']


class ExtraOptionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основное', {'fields': ('name', 'cost', 'categories')}),
        ('Дополнительно', {'fields': ('slug', 'custom_slug')}),
    )


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductListFilter(admin.SimpleListFilter):
    title = ('Category')
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        qs = Category.objects.all()
        for category in qs:
            if category.get_descendant_count() == 0:
                yield ([category.id], (f'{category.name}'))
            else:
                children = [child.id for child in category.get_descendants()]
                yield (children, (category.name))

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset
        else:
            print(
                list(map(int, value.replace('[', '').replace(']', '').split(', '))))
            return queryset.filter(category__id__in=list(map(int, value.replace('[', '').replace(']', '').split(', '))))


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_price', 'price',
                    'stock_availability', 'not_in_stock', 'category')

    def formfield_for_foreignkey(sf, db_field, request, **kwargs):
        print(sf, db_field, request, **kwargs)
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.filter(
                children=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        ('Категория', {'fields': ('category', 'brand',)}),
        ('Главное изображение', {'fields': ('main_image',)}),
        ('Основная информация', {
         'fields': ('sku', 'name', 'price', 'discount_price', 'price_in_dollars', 'stock_availability', 'not_in_stock', 'description', )}),
        ('Дополнительно', {
            'classes': ('collapse',),
            'fields': ('custom_slug', 'slug', 'published'),
        }),
        ('SEO', {
            'fields': ('page_title', 'meta_description',),
        }),
    )
    search_fields = ['sku', 'name', 'brand__name', 'category__name', ]
    list_filter = (ProductListFilter,)
    readonly_fields = ('published', 'sku')
    inlines = [PropertyValueInline, ProductImageInline]


class CategoryListFilter(admin.SimpleListFilter):
    title = ('parent')
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        qs_filtered = qs.filter()

        for query_instance in qs_filtered:
            yield (f'{query_instance.name}', (f'{query_instance.name}'))

    def queryset(self, request, queryset):
        category = self.value()
        if category is None:
            return queryset
        return queryset.filter(parent__name=f'{category}')


class CategoryMPTTModelAdmin(DraggableMPTTAdmin):
    fieldsets = (
        ('Основное', {'fields': ('name', 'image',
                                 'parent', 'description')}),
        ('Дополнительные настройки', {
            'classes': ('collapse',),
            'fields': ('custom_slug', 'slug'),
        }),
        ('Настройки отображения', {
            'classes': ('collapse',),
            'fields': ('show_on_the_homepage_at_the_footer', 'show_brands_in_the_menu', 'additional_parents',),
        }),
        ('SEO', {'fields': ('page_title', 'meta_description',
                            'where_to_insert_dynamic_page_title_data', 'where_to_insert_dynamic_meta_description_data')}),
        ('Доставка', {'fields': ('delievery_cost',
                                 'count_delievery_cost_for_each_product',), })
    )
    filter_horizontal = ['additional_parents']
    search_fields = ['name']


class PropertyAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories',)
    search_fields = ['name']


class BrandAdmin(admin.ModelAdmin):
    search_fields = ['name']


class PaymentAndDelieveryOptionsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основное', {'fields': ('name', 'description')}),
        ('Дополнительные настройки', {"fields": ('slug',)}),

    )


class DelieveryCityOptionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Основное', {'fields': ('name',)}),
        ('Дополнительные настройки', {'fields': ('custom_slug', 'slug',)})
    )


admin.site.register(MoneyRate)
admin.site.register(BillingAddress)
admin.site.register(DelieveryOption, PaymentAndDelieveryOptionsAdmin)
admin.site.register(DelieveryCityOption, DelieveryCityOptionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(BasketProduct)
admin.site.register(Basket)
admin.site.register(Category, CategoryMPTTModelAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyValue, PropertyValueAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Page)
admin.site.register(PaymentOption, PaymentAndDelieveryOptionsAdmin)
admin.site.register(ProductView)
admin.site.register(ProductImage)
admin.site.register(ProductReview)
admin.site.register(OrderedBasket)
admin.site.register(HotProduct)
admin.site.register(HomePageBannerImage)
admin.site.register(CustomerRequestToCallBack)
admin.site.register(ExtraOption, ExtraOptionAdmin)
