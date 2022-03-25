# Generated by Django 3.0.6 on 2020-10-08 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0196_extraoptionordered_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='extraoptionordered',
            name='count',
            field=models.IntegerField(blank=True, null=True, verbose_name='Количество заказанной опции'),
        ),
        migrations.AlterField(
            model_name='extraoptionordered',
            name='basket_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.BasketProduct', verbose_name='Продукт заказанной опции'),
        ),
        migrations.AlterField(
            model_name='extraoptionordered',
            name='name',
            field=models.CharField(max_length=55, verbose_name='Название заказанной опции'),
        ),
        migrations.AlterField(
            model_name='extraoptionordered',
            name='slug',
            field=models.SlugField(blank=True, max_length=55, null=True, verbose_name='Slug заказанной опции'),
        ),
    ]
