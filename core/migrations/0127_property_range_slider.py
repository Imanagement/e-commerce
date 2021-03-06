# Generated by Django 3.0.5 on 2020-07-07 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0126_auto_20200703_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='range_slider',
            field=models.BooleanField(default=False, help_text='Поле, которое указывает, отображать значения этого свойства на страницах с фильтрами как список значений или как диапазон, например, как цена.', verbose_name='Отображать как диапазон значений'),
        ),
    ]
