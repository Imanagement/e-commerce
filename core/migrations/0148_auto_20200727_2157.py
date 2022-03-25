# Generated by Django 3.0.5 on 2020-07-27 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0147_auto_20200727_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='meta_description',
            field=models.TextField(default='', verbose_name='Meta Description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='page_title',
            field=models.CharField(default='', max_length=155, verbose_name='Page title'),
            preserve_default=False,
        ),
    ]
