# Generated by Django 3.0.5 on 2020-05-28 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_auto_20200528_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_level',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=55, null=True),
        ),
    ]
