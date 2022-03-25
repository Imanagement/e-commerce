# Generated by Django 3.0.6 on 2020-10-15 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0198_moneyrate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_in_dollars',
            field=models.FloatField(default=0, verbose_name='Цена в долларах'),
            preserve_default=False,
        ),
    ]