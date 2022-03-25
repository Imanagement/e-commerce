# Generated by Django 3.0.5 on 2020-07-02 12:52

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0117_auto_20200702_1542'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterField(
            model_name='category',
            name='additional_parents',
            field=models.ManyToManyField(help_text='Относится только к меню. Список категорий, под которыми отображать данную категорию как дочернюю.', to='core.Category', verbose_name='Дополнительные родители'),
        ),
        migrations.AlterField(
            model_name='category',
            name='custom_slug',
            field=models.BooleanField(default=False, help_text='Поле, которое указывает, перезаписывать ли slug(строка в URL) или оставить автоматическое сохранение. Это необходимо, если категория с таким же slug уже есть, так как невозможно сохранить две и более категории с одинаковым slug. В ином случае нет необходимости вводить собственный slug.', verbose_name='Собственный slug'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(upload_to='', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, help_text='Строка в URL, по которой можно найти категорию. Заполняется автоматически во время сохранения страницы. Если поле "Собственный slug" включено, то необходимо вручную ввести сюда свой slug в формате: eto-moi-slug.', max_length=55, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Brand', verbose_name='Бренд'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='custom_slug',
            field=models.BooleanField(default=False, help_text='Поле, которое указывает, перезаписывать ли slug(строка в URL) или оставить автоматическое сохранение. Это необходимо, если категория с таким же slug уже есть, так как невозможно сохранить две и более категории с одинаковым slug. В ином случае нет необходимости вводить собственный slug.', verbose_name='Собственный slug'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.FloatField(blank=True, help_text='Если указана скидочная цена, она будет отражаться вместо обычной цены.', null=True, verbose_name='Скидочная цена'),
        ),
        migrations.AlterField(
            model_name='product',
            name='main_image',
            field=imagekit.models.fields.ProcessedImageField(upload_to='', verbose_name='Главное изображение'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='product',
            name='published',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(max_length=8, verbose_name='SKU'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, help_text='Строка в URL, по которой можно найти категорию. Заполняется автоматически во время сохранения страницы. Если поле "Собственный slug" включено, то необходимо вручную ввести сюда свой slug в формате: eto-moi-slug.', null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='views_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='Количество просмотров'),
        ),
    ]
