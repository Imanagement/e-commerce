# Generated by Django 3.0.5 on 2020-07-21 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0143_auto_20200720_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='weight',
            field=models.IntegerField(default=0, help_text='Чем выше вес свйоства, тем выше оно будет в списке фильтров и в списке свойств на страницах товаров ', verbose_name='Вес категории'),
            preserve_default=False,
        ),
    ]