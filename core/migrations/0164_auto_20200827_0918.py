# Generated by Django 3.0.6 on 2020-08-27 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0163_auto_20200827_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delieverycityoption',
            name='slug',
            field=models.SlugField(blank=True, max_length=25, null=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='delieveryoption',
            name='slug',
            field=models.SlugField(blank=True, max_length=55, null=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='paymentoption',
            name='slug',
            field=models.SlugField(blank=True, max_length=35, null=True, verbose_name='Slug'),
        ),
    ]