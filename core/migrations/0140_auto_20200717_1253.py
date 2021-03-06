# Generated by Django 3.0.5 on 2020-07-17 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0139_auto_20200716_1404'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='propertyvalue',
            options={'verbose_name': 'Свойство товара со значением', 'verbose_name_plural': 'Свойства товара со значением'},
        ),
        migrations.AddField(
            model_name='propertyvalue',
            name='int_value_of_value',
            field=models.IntegerField(default=0, help_text="Численное значение, которое берется из поля 'Значение'. Заполняется автоматически во время сохранения страницы.", verbose_name='Численное значение'),
            preserve_default=False,
        ),
    ]
