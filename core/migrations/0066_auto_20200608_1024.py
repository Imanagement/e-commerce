# Generated by Django 3.0.5 on 2020-06-08 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0065_property_custom_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='propertyvalue',
            options={'ordering': ['value'], 'verbose_name': 'PropertyValue', 'verbose_name_plural': 'PropertyValues'},
        ),
    ]
