# Generated by Django 3.0.6 on 2020-10-08 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0194_auto_20201006_0805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extraoptionordered',
            name='product',
        ),
        migrations.AddField(
            model_name='extraoptionordered',
            name='basket_product',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='core.BasketProduct', verbose_name='Продукт'),
            preserve_default=False,
        ),
    ]
