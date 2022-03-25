# Generated by Django 3.0.5 on 2020-07-02 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0123_auto_20200702_1722'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'verbose_name': 'Изображение товара', 'verbose_name_plural': 'Изображения товара'},
        ),
        migrations.AlterModelOptions(
            name='productview',
            options={'verbose_name': 'Просмотр продукта', 'verbose_name_plural': 'Просмотры продукта'},
        ),
        migrations.AlterModelOptions(
            name='propertyvalue',
            options={'verbose_name': 'Свойство товара со значением', 'verbose_name_plural': 'Свойства товара со значением'},
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='city_address',
            field=models.CharField(max_length=2, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='first_name',
            field=models.CharField(max_length=35, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='last_name',
            field=models.CharField(max_length=35, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='phone',
            field=models.CharField(max_length=35, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='postcode',
            field=models.CharField(max_length=15, verbose_name='Почтовый индекс'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='street_address',
            field=models.CharField(max_length=100, verbose_name='Улица'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Зарегистрированный покупатель'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(upload_to='', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Product', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='productview',
            name='ip',
            field=models.CharField(max_length=50, verbose_name='IP обозревателя'),
        ),
        migrations.AlterField(
            model_name='productview',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Product', verbose_name='Продукт'),
        ),
    ]