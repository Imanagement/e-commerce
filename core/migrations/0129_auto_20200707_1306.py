# Generated by Django 3.0.5 on 2020-07-07 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0128_auto_20200707_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='categories',
            field=models.ManyToManyField(help_text='Список категорий, к которым будет относится свойство', to='core.Category', verbose_name='Категории'),
        ),
    ]
