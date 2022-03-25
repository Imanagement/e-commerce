# Generated by Django 3.0.5 on 2020-07-01 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0107_auto_20200701_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='show_brands_in_the_menu',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='additional_parents',
            field=models.ManyToManyField(related_name='_category_additional_parents_+', to='core.Category', verbose_name='Дополнительные родители'),
        ),
    ]