# Generated by Django 3.0.5 on 2020-06-11 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0074_brand_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='name',
            field=models.CharField(max_length=35),
        ),
        migrations.AlterField(
            model_name='property',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]