# Generated by Django 3.0.5 on 2020-07-07 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0131_auto_20200707_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
    ]
