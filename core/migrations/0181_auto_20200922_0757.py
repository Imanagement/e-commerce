# Generated by Django 3.0.6 on 2020-09-22 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0180_auto_20200914_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price_in_dollars',
            field=models.FloatField(blank=True, null=True, verbose_name='Цена в долларах'),
        ),
    ]
