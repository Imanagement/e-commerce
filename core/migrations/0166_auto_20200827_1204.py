# Generated by Django 3.0.6 on 2020-08-27 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0165_auto_20200827_1159'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='billingaddress',
            options={'verbose_name': 'Адрес доставки', 'verbose_name_plural': 'Адреса доставки'},
        ),
    ]