# Generated by Django 3.0.5 on 2020-12-29 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0203_auto_20201030_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderedbasket',
            name='delivery_option',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.DelieveryOption', verbose_name='Выбранный способ доставки'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderedbasket',
            name='payment_option',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='core.PaymentOption', verbose_name='Выбранный способ оплаты'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderedbasket',
            name='delievery_payment',
            field=models.IntegerField(null=True, verbose_name='Стоимость доставки'),
        ),
    ]
