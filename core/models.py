from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db import connection, models, IntegrityError
from django.db.models.signals import pre_save, post_save
from django.shortcuts import reverse, redirect
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.text import slugify
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from mptt.models import MPTTModel, TreeForeignKey
from tinymce import models as tinymce_models
from transliterate import translit
import re
import sys


class MoneyRate(models.Model):
    money_rate = models.FloatField(verbose_name="Курс")

    class Meta:
        verbose_name = ('Курс')
        verbose_name_plural = ('Курс')

    def save(self):
        try:
            super().save()
            products = Product.objects.all()
            for p in products:
                p.save()
        except Exception:
            raise Exception()

    def __str__(self):
        return f"Курс {self.money_rate}"


class Brand(models.Model):

    name = models.CharField(max_length=25, verbose_name="Имя")
    category = models.ManyToManyField('Category', verbose_name="Категория")

    class Meta:
        verbose_name = ("Бренд")
        verbose_name_plural = ("Бренды")

    def __str__(self):
        return self.name


class Category(MPTTModel):
    """ Category model with inheritance of MPTTModel in django-mptt package for optimized data tree structure. """
    name = models.CharField(max_length=55, verbose_name="Имя")
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Родительская категория")
    custom_slug = models.BooleanField(default=False, verbose_name="Собственный slug",
                                      help_text="Поле, которое указывает, перезаписывать ли slug(строка в URL) или оставить автоматическое сохранение. Это необходимо, если категория с таким же slug уже есть, так как невозможно сохранить две и более категории с одинаковым slug. В ином случае нет необходимости вводить собственный slug.")
    slug = models.SlugField(max_length=55, null=True, blank=True, unique=True, verbose_name="Slug",
                            help_text="Строка в URL, по которой можно найти категорию. Заполняется автоматически во время сохранения страницы. Если поле \"Собственный slug\" включено, то необходимо вручную ввести сюда свой slug в формате: eto-moi-slug.")
    image = ProcessedImageField(
        processors=[ResizeToFill(700, 700)], format='JPEG', options={'quality': 60}, verbose_name="Изображение")
    show_on_the_homepage_at_the_footer = models.BooleanField(
        default=False, verbose_name="Показать категорию в подвале на главной странице")
    additional_parents = models.ManyToManyField(
        "self", symmetrical=False, blank=True, verbose_name="Дополнительные родители", help_text="Относится только к меню. Список категорий, под которыми отображать данную категорию как дочернюю.")
    show_brands_in_the_menu = models.BooleanField(
        default=False, verbose_name="Показать бренды в меню")
    description = models.TextField(
        _("Описание категории"), help_text="Текст отоброжающийся внизу страницы категории", null=True, blank=True)
    delievery_cost = models.IntegerField(
        verbose_name="Цена за доставку товара", default=0, null=True, blank=True)
    count_delievery_cost_for_each_product = models.BooleanField(
        default=False, verbose_name="Считать доставку за каждый товар")

    # SEO
    page_title = models.CharField(
        _("Page title"), max_length=155, null=True, blank=True)
    meta_description = models.TextField(
        _("Meta Description"), null=True, blank=True)
    where_to_insert_dynamic_page_title_data = models.IntegerField(
        'Местоположение динамеческих свойств в title', help_text="После какого слова в title вставлять динамические свойства", null=True, blank=True)
    where_to_insert_dynamic_meta_description_data = models.IntegerField(
        'Местоположение динамеческих свойств в description', help_text="После какого слова в description вставлять динамические свойства", null=True, blank=True)

    class Meta:
        verbose_name = ("Категория")
        verbose_name_plural = ("Категории")

    def get_absolute_url(self):
        return reverse('core:categories-list' if self.get_descendant_count() != 0 else 'core:category-view', kwargs={
            'slug': self.slug
        })

    def save(self):
        try:
            self.slug = slugify(
                translit(self.name, 'ru', reversed=True)) if self.custom_slug is False else self.slug
            if len(self.slug) <= 0:
                raise Exception(
                    'Возникла непредвиденная ошибка. Пожалуйста, свяжитесь с системным администратором.')

            if self.where_to_insert_dynamic_page_title_data:
                if len(self.page_title.split(' ')) < self.where_to_insert_dynamic_page_title_data:
                    raise Exception(
                        'Местоположение динамеческих свойств в title не может быть меньше количества слов в Page title')
            if self.where_to_insert_dynamic_meta_description_data:
                if len(self.meta_description.split(' ')) < self.where_to_insert_dynamic_meta_description_data:
                    raise Exception(
                        'Местоположение динамеческих свойств в description не может быть меньше количества слов в Meta Description')
            key = make_template_fragment_key('vertical_menu')
            if self.count_delievery_cost_for_each_product and self.get_descendants():
                for category in self.get_descendants():
                    category.count_delievery_cost_for_each_product = True
                    category.delievery_cost = self.delievery_cost
                    category.save()
            cache.delete(key)
            super().save()
        except Exception as e:
            raise Exception(
                'Возникла непредвиденная ошибка. Пожалуйста, свяжитесь с системным администратором.')

    def __str__(self):
        return self.name


class HotProduct(models.Model):
    """ Model of 1 hot product on the homepage """

    product = models.OneToOneField(
        'Product', verbose_name='Продукт', on_delete=models.CASCADE, null=True)
    deal_end_date = models.DateTimeField(
        verbose_name='Длительность предложениия', null=True)

    class Meta:
        verbose_name = ("Горящее предложение")
        verbose_name_plural = ("Горящие предложения")

    def __str__(self):
        return f"{self.product.name} - Горячее предложение"


class Product(models.Model):

    name = models.CharField(max_length=155, verbose_name="Имя")
    price = models.IntegerField(verbose_name="Цена", null=True, blank=True)
    discount_price = models.IntegerField(null=True, blank=True, verbose_name="Скидочная цена",
                                         help_text="Если указана скидочная цена, она будет отражаться вместо обычной цены.")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    price_in_dollars = models.FloatField(
        verbose_name="Цена в долларах", null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, verbose_name="Бренд")
    custom_slug = models.BooleanField(default=False, verbose_name="Собственный slug",
                                      help_text="Поле, которое указывает, перезаписывать ли slug(строка в URL) или оставить автоматическое сохранение. Это необходимо, если категория с таким же slug уже есть, так как невозможно сохранить две и более категории с одинаковым slug. В ином случае нет необходимости вводить собственный slug.")
    slug = models.SlugField(max_length=155, null=True, blank=True, verbose_name="Slug",
                            help_text="Строка в URL, по которой можно найти категорию. Заполняется автоматически во время сохранения страницы. Если поле \"Собственный slug\" включено, то необходимо вручную ввести сюда свой slug в формате: eto-moi-slug.")
    description = RichTextUploadingField(verbose_name="Описание")
    main_image = ProcessedImageField(
        processors=[ResizeToFill(700, 700)], format='JPEG', options={'quality': 80}, verbose_name="Главное изображение")
    main_image_thumbnail = ImageSpecField(
        processors=[ResizeToFill(228, 228)], format='JPEG', options={'quality': 80})
    published = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации")
    views_count = models.IntegerField(
        null=True, blank=True, editable=True, verbose_name="Количество просмотров")
    sku = models.CharField(max_length=8, verbose_name="SKU")
    stock_availability = models.IntegerField(verbose_name="Количество товара в наличии",
                                             help_text="Если количество товара равно 0, товар будет помечен серым цветом.")
    not_in_stock = models.BooleanField(default=False, verbose_name="Нет на складе",
                                       help_text="Если помечено галочкой, наличие товара будет отображаться \"На складах компании\" ")

    # SEO
    page_title = models.CharField(
        _("Page title"), max_length=155, null=True, blank=True)
    meta_description = models.TextField(
        _("Meta Description"), null=True, blank=True)

    class Meta:
        verbose_name = ("Продукт")
        verbose_name_plural = ("Продукты")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            self.slug = slugify(
                translit(self.name, 'ru', reversed=True)) if self.custom_slug is False else self.slug
            if len(self.slug) <= 0:
                raise Exception(
                    'Возникла непредвиденная ошибка со slug. Пожалуйста, свяжитесь с системным администратором.')
            self.sku = '0' * (8 - len(str(self.id))) + str(self.id)
            money_rate = MoneyRate.objects.first()
            if money_rate and self.price_in_dollars:
                self.price = self.price_in_dollars * MoneyRate.objects.first().money_rate
            super().save()
        except Exception:
            type, value, traceback = sys.exc_info()
            raise Exception(value)

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

    def get_product_leave_review_url(self):
        return reverse("core:leave-product-review", kwargs={
            'slug': self.slug
        })

    def get_add_to_compare_url(self):
        return reverse("core:add-to-compare", kwargs={
            'slug': self.slug
        })

    def get_remove_from_compare_url(self):
        return reverse("core:remove-from-compare", kwargs={
            'slug': self.slug
        })

    def get_add_to_wishlist_url(self):
        return reverse("core:add-to-wishlist", kwargs={
            'slug': self.slug
        })

    def get_remove_from_wishlist_url(self):
        return reverse("core:remove-from-wishlist", kwargs={
            'slug': self.slug
        })

    def get_all_reviews_url(self):
        return reverse("core:get-all-reviews", kwargs={
            'slug': self.slug
        })


class ProductReview(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, verbose_name="Продукт")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE, null=True, blank=True, verbose_name="Зарегистрированный покупатель")
    customer_ip = models.CharField(max_length=50, verbose_name="IP адрес")
    customer_session = models.CharField(max_length=50, verbose_name="Номер сессии",
                                        help_text="Номер сессии это отличительный это номер сеанса пользователя")
    customer_name = models.CharField(max_length=50, verbose_name="Имя")
    customer_email = models.EmailField(max_length=254, verbose_name="Email")
    customer_review = models.FloatField(verbose_name="Оценка")
    customer_review_text = models.TextField(
        max_length=255, verbose_name="Отзыв")
    published = models.BooleanField(default=False, verbose_name="Опубликовать",
                                    help_text="Показывать ли этот отзыв на странице с продуктом.")
    publish_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = ("Отзыв покупателя")
        verbose_name_plural = ("Отзывы покупателей")

    def __str__(self):
        return f"{self.product} Комментарий от {self.customer_name}"


class BasketProduct(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True, verbose_name="Зарегистрированный покупатель")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.IntegerField(
        default=1, verbose_name="Количество продукта")
    is_ordered = models.BooleanField(default=False, verbose_name="Заказан")
    which_basket = models.ManyToManyField(
        'Basket', blank=True, verbose_name="Заказ")

    class Meta:
        verbose_name = ("Продукт в корзине")
        verbose_name_plural = ("Продукты в корзинах")

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_summary(self):
        return self.product.price * self.quantity

    def get_total_discount_summary(self):
        return self.product.discount_price * self.quantity


class Basket(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True, verbose_name="Зарегистрированный покупатель")
    products = models.ManyToManyField(BasketProduct, verbose_name="Продукты")
    start_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата открытия корзины")
    ordered_date = models.DateTimeField(verbose_name="Дата заказа корзины")
    basket_changed_date = models.DateField(
        verbose_name="Дата изменения корзины", null=True, blank=True)
    is_ordered = models.BooleanField(default=False, verbose_name='Заказан')

    class Meta:
        verbose_name = ("Корзина")
        verbose_name_plural = ("Корзины")

    def __str__(self):
        if self.user:
            return f"Заказ  #{self.pk} от {self.user}"
        else:
            return f"Заказ(Анонимный) #{self.pk}"

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})


class OrderedBasket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True, verbose_name="Зарегистрированный покупатель")
    basket = models.OneToOneField(
        'Basket', on_delete=models.SET_NULL, verbose_name="Корзина", null=True)
    ordered_date = models.DateTimeField(verbose_name="Дата оформления заказа")
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Адрес для выставления счета")
    total_summary = models.IntegerField(
        verbose_name="Общая стоимость корзины")
    delivery_option = models.ForeignKey('DelieveryOption', on_delete=models.CASCADE, verbose_name="Выбранный способ доставки")
    payment_option = models.ForeignKey('PaymentOption', on_delete=models.CASCADE, verbose_name='Выбранный способ оплаты')
    delievery_payment = models.IntegerField(
        verbose_name="Стоимость доставки", null=True, )
    customer_wants_credit = models.BooleanField(
        default=False, verbose_name='Покупатель оформил в кредит')
    credit_duration = models.IntegerField(
        verbose_name="Количество месяцев для кредита", null=True, blank=True)
    credit_month_payment = models.IntegerField(
        verbose_name="Стоимость ежемесячного взноса", null=True, blank=True)

    class Meta:
        verbose_name = ('Заказ')
        verbose_name_plural = ('Оформленные заказы')

    def __str__(self):
        return f"Заказ корзины #{self.basket.id}"


class Property(models.Model):

    name = models.CharField(max_length=155, verbose_name='Имя')
    custom_slug = models.BooleanField(default=False, verbose_name="Собственный slug",
                                      help_text="Поле, которое указывает, перезаписывать ли slug(строка в URL) или оставить автоматическое сохранение. Это необходимо, если категория с таким же slug уже есть, так как невозможно сохранить две и более категории с одинаковым slug. В ином случае нет необходимости вводить собственный slug.")
    slug = models.SlugField(max_length=155, null=True, blank=True, unique=True, verbose_name="Slug",
                            help_text="Строка в URL, по которой можно найти категорию. Заполняется автоматически во время сохранения страницы. Если поле \"Собственный slug\" включено, то необходимо вручную ввести сюда свой slug в формате: eto-moi-slug.")
    categories = models.ManyToManyField(
        Category, verbose_name="Категории", help_text="Список категорий, к которым будет относится свойство")
    range_slider = models.BooleanField(default=False, verbose_name="Отображать как диапазон значений",
                                       help_text="Поле, которое указывает, отображать значения этого свойства на страницах с фильтрами как список значений или как диапазон, например, как цена.")
    weight = models.IntegerField(verbose_name="Вес категории",
                                 help_text="Чем выше вес свойства, тем выше оно будет в списке фильтров и в списке свойств на страницах товаров ")
    dynamic_seo = models.BooleanField(verbose_name='Динамическое SEO в категориях', default=False,
                                      help_text="Автоматически вставлять свойство в title и description при фильтрации категорий.")

    def save(self, *args, **kwargs):
        try:
            self.slug = slugify(
                translit(self.name, 'ru', reversed=True)) if self.custom_slug is False else self.slug
            if len(self.slug) <= 0:
                raise Exception(
                    'Пожалуйста, выберите другое имя для Вашего свойства.')
            super().save()
        except IntegrityError:
            raise IntegrityError(
                'Невозможно создать данное свойство, так как оно уже существует, пожалуйста найдите его и привяжите к желаемой категории.'
            )
        except Exception:
            raise Exception(
                'Возникла непредвиденная ошибка. Пожалуйста, свяжитесь с системным администратором.')

    class Meta:
        verbose_name = ("Свойство товаров")
        verbose_name_plural = ("Свойства товаров")
        ordering = ['weight']

    def __str__(self):
        return self.name

    @property
    def sorted_property_values_set(self):
        return self.propertyvalue_set.all().order_by('int_value_of_value', 'value')


class PropertyValue(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, verbose_name="Продукт")
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, verbose_name="Свойство")
    value = models.CharField(max_length=55, verbose_name="Значение")
    custom_slug = models.BooleanField(default=False, verbose_name="Собственный slug",
                                      help_text="Поле, которое указывает, перезаписывать ли slug(строка в URL) или оставить автоматическое сохранение. Это необходимо, если категория с таким же slug уже есть, так как невозможно сохранить две и более категории с одинаковым slug. В ином случае нет необходимости вводить собственный slug.")
    slug = models.SlugField(max_length=155, null=True, blank=True, verbose_name="Slug",
                            help_text="Строка в URL, по которой можно найти категорию. Заполняется автоматически во время сохранения страницы. Если поле \"Собственный slug\" включено, то необходимо вручную ввести сюда свой slug в формате: eto-moi-slug.")
    int_value_of_value = models.FloatField(null=True, blank=True,
                                           verbose_name="Численное значение", help_text="Численное значение, которое берется из поля 'Значение'. Заполняется автоматически во время сохранения страницы.")

    def save(self, *args, **kwargs):
        try:
            self.slug = slugify(
                f"{translit(self.property.name, 'ru', reversed=True)}-{translit(self.value, 'ru', reversed=True)}") if self.custom_slug is False else self.slug
            if len(self.slug) <= 0:
                raise Exception(
                    'Возникла непредвиденная ошибка. Пожалуйста, свяжитесь с системным администратором.')
            try:
                self.int_value_of_value = int(re.findall(
                    r"[-+]?\d*\.\d+|\d+", self.value)[0])
            except ValueError:
                self.int_value_of_value = float(re.findall(
                    r"[-+]?\d*\.\d+|\d+", self.value)[0])
            except Exception:
                self.int_value_of_value = None
            if not self.int_value_of_value:
                self.int_value_of_value = None
            super().save()
        except Exception:
            raise Exception(
                'Возникла непредвиденная ошибка. Пожалуйста, свяжитесь с системным администратором.')

    class Meta:
        ordering = ['int_value_of_value', 'value']
        verbose_name = ("Свойство товара со значением")
        verbose_name_plural = ("Свойства товара со значением")

    def __str__(self):
        return f"{str(self.property)} - {str(self.value)}"


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт")
    image = ProcessedImageField(
        processors=[ResizeToFill(700, 700)], format='JPEG', options={'quality': 80}, verbose_name="Изображение")

    class Meta:
        verbose_name = ("Изображение товара")
        verbose_name_plural = ("Изображения товара")

    def __str__(self):
        return f"{self.product} - Изображение"

    def get_url(self):
        return self.image.url

    def get_absolute_url(self):
        return reverse("ProductImage_detail", kwargs={"pk": self.pk})


class ProductView(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт")
    ip = models.CharField(max_length=50, verbose_name="IP обозревателя")

    class Meta:
        verbose_name = ("Просмотр продукта")
        verbose_name_plural = ("Просмотры продукта")

    def __str__(self):
        return f"{self.product} - кол-во просмотров"


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True, verbose_name="Зарегистрированный покупатель")
    customer_first_name = models.CharField(max_length=35, verbose_name="Имя")
    last_name = models.CharField(max_length=35, verbose_name="Фамилия")
    street_address = models.CharField(max_length=100, verbose_name="Улица")
    city_address = models.ForeignKey(
        'DelieveryCityOption', verbose_name="Город", on_delete=models.CASCADE)
    postcode = models.CharField(max_length=15, verbose_name="Почтовый индекс")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=35, verbose_name="Телефон")
    delievery_option = models.ForeignKey(
        'DelieveryOption', verbose_name="Способ доставки", on_delete=models.CASCADE)
    payment_option = models.ForeignKey(
        'PaymentOption', verbose_name="Способ оплаты", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ('Адрес доставки')
        verbose_name_plural = ('Адреса доставки')

    def __str__(self):
        return f"Адрес #{self.id} заказа от {self.customer_first_name} {self.last_name}"


class HomePageBannerImage(models.Model):
    banner_image = ProcessedImageField(
        processors=[ResizeToFill(1400, 450)], format='JPEG', options={'quality': 100}, verbose_name="Изображение на баннере")
    category_follow_to = models.ForeignKey(Category, null=True, verbose_name=_(
        "Категория"), on_delete=models.CASCADE, help_text="Категория которая будет открываться при клике на баннер")

    class Meta:
        verbose_name = ("Баннер")
        verbose_name_plural = ("Баннеры")

    def __str__(self):
        return f"{self.id} Баннер"


class CustomerRequestToCallBack(models.Model):
    phone = models.CharField(max_length=15, verbose_name="Номер телефона")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 null=True, blank=True, verbose_name="Зарегистрированный покупатель")
    ip = models.CharField(max_length=32)
    name = models.CharField(max_length=32, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    customer_called_back = models.BooleanField(
        default=False, verbose_name="Клиенту перезвонили?")

    class Meta:
        verbose_name = ('Запрос на звонок')
        verbose_name_plural = ('Запросы на звонок')

    def __str__(self):
        return str(self.phone)


class PaymentOption(models.Model):
    name = models.CharField(
        max_length=55, verbose_name="Название способа оплаты")
    description = models.CharField(
        max_length=355, verbose_name="Описание способа оплаты")
    slug = models.SlugField(
        max_length=35, verbose_name="Slug", null=True, blank=True, unique=True)
    custom_slug = models.BooleanField(
        default=False, verbose_name="Собственный Slug")

    class Meta:
        verbose_name = ('Способ оплаты')
        verbose_name_plural = ('Способы оплаты')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            if self.custom_slug:
                self.slug = slugify(
                    translit(self.name, 'ru', reversed=True))
                if len(self.slug) <= 0:
                    raise Exception(
                        'Возникла непредвиденная ошибка со slug. Пожалуйста, свяжитесь с системным администратором.')
            super().save()
        except Exception:
            raise Exception(
                'Возникла непредвиденная ошибка. Пожалуйста, свяжитесь с системным администратором.')


class DelieveryOption(models.Model):
    name = models.CharField(
        max_length=55, verbose_name="Название способа доставки")
    description = models.CharField(
        max_length=355, verbose_name="Описание способа доставки")
    slug = models.SlugField(
        max_length=55, verbose_name="Slug", null=True, blank=True, unique=True)
    custom_slug = models.BooleanField(
        default=False, verbose_name="Собственный Slug")

    class Meta:
        verbose_name = ('Способ доставки')
        verbose_name_plural = ('Способы доставки')

    def __str__(self):
        return self.name

    def save(self):
        try:
            if self.custom_slug:
                self.slug = slugify(
                    translit(self.name, 'ru', reversed=True))
                if len(self.slug) <= 0:
                    raise Exception(
                        'Возникла непредвиденная ошибка со slug. Пожалуйста, свяжитесь с системным администратором.')
            super().save()
        except Exception:
            raise Exception(
                'Возникла непредвиденная ошибка. Пожалуйста, свяжитесь с системным администратором.')


class DelieveryCityOption(models.Model):
    name = models.CharField(max_length=25, verbose_name="Название города")
    slug = models.SlugField(
        max_length=25, verbose_name="Slug", null=True, blank=True)
    custom_slug = models.BooleanField(
        default=False, verbose_name="Собственный Slug")

    class Meta:
        verbose_name = ('Доступный для доставки город')
        verbose_name_plural = ('Доступные для доставки города')

    def __str__(self):
        return self.name

    def save(self):
        try:
            if self.custom_slug:
                self.slug = slugify(
                    translit(self.name, 'ru', reversed=True))
                if len(self.slug) <= 0:
                    raise Exception(
                        'Возникла непредвиденная ошибка со slug. Пожалуйста, свяжитесь с системным администратором.')
            super().save()
        except Exception:
            raise Exception(
                'Возникла непредвиденная ошибка. Пожалуйста, свяжитесь с системным администратором.')


class Page(models.Model):
    name = models.CharField(max_length=25, verbose_name="Название страницы")
    slug = models.CharField(max_length=30, verbose_name="Slug страницы",
                            help_text="Slug - текст в адресе страницы после tehnomall.md например slug для \"Контакты\": /kontakti ")
    page_title = models.CharField(
        max_length=155, verbose_name="Title страницы", null=True, blank=True)
    meta_description = models.TextField(
        verbose_name="Meta description страницы", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ('SEO страницы')
        verbose_name_plural = ('SEO страниц')


class ExtraOption(models.Model):
    name = models.CharField(
        max_length=55, verbose_name="Название дополнительной опции")
    slug = models.SlugField(
        max_length=55, verbose_name="Slug дополнительной опции", null=True, blank=True)
    custom_slug = models.BooleanField(default=False, verbose_name="Собственный slug",
                                      help_text="Поле, которое указывает, перезаписывать ли slug(строка в URL) или оставить автоматическое сохранение. Это необходимо, если категория с таким же slug уже есть, так как невозможно сохранить две и более категории с одинаковым slug. В ином случае нет необходимости вводить собственный slug.")
    categories = models.ManyToManyField(
        Category, verbose_name="Категории дополнительной опции")
    cost = models.IntegerField(verbose_name="Стоимость дополнительной опции")

    def save(self):
        try:
            self.slug = slugify(
                translit(self.name, 'ru', reversed=True)) if self.custom_slug is False else self.slug
            if len(self.slug) <= 0:
                raise Exception(
                    'Возникла непредвиденная ошибка. Пожалуйста, свяжитесь с системным администратором.')
            super().save()
        except Exception:
            raise Exception()

    def __str__(self):
        return f"Дополнительная опция: {self.name}"

    class Meta:
        verbose_name = ('Дополнительная опция')
        verbose_name_plural = ('Дополнительные опции')


class ExtraOptionOrdered(models.Model):
    name = models.CharField(
        max_length=55, verbose_name="Название заказанной опции")
    cost = models.IntegerField(verbose_name='Стоимость опции')
    count = models.IntegerField(
        verbose_name='Количество заказанной опции', null=True, blank=True)
    slug = models.SlugField(
        max_length=55, verbose_name="Slug заказанной опции", null=True, blank=True)
    custom_slug = models.BooleanField(default=False, verbose_name="Собственный slug",
                                      help_text="Поле, которое указывает, перезаписывать ли slug(строка в URL) или оставить автоматическое сохранение. Это необходимо, если категория с таким же slug уже есть, так как невозможно сохранить две и более категории с одинаковым slug. В ином случае нет необходимости вводить собственный slug.")
    basket_product = models.ForeignKey(
        BasketProduct, verbose_name="Продукт заказанной опции", on_delete=models.CASCADE)
    option = models.ForeignKey(
        ExtraOption, verbose_name="Опция", on_delete=models.CASCADE)

    def __str__(self):
        return f"Опция {self.name} для {self.basket_product}"

    def get_total_summary(self):
        return self.cost * self.count

    class Meta:
        verbose_name = ('Заказанная опция для продукта')
        verbose_name_plural = ('Заказанные опции для продуктов')


@receiver(post_save, sender=Product)
def set_product_sku(sender, instance, **kwargs):
    instance.sku = str('0' * (8 - len(str(instance.id))))


def natural_sort(list):
    def convert(text):
        return int(text[0]) if text[0].isdigit() else text[0].lower()

    def alphanum_key(key):
        return [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(list, key=alphanum_key)
