# Generated by Django 3.0.5 on 2020-07-21 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0144_property_weight'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='property',
            options={'ordering': ['weight'], 'verbose_name': 'Свойство товаров', 'verbose_name_plural': 'Свойства товаров'},
        ),
    ]
