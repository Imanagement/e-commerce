# Generated by Django 3.0.5 on 2020-06-26 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0094_remove_product_extra_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productview',
            name='session',
        ),
        migrations.DeleteModel(
            name='MttpTestClass',
        ),
    ]
