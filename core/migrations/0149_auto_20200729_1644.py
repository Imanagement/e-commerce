# Generated by Django 3.0.5 on 2020-07-29 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0148_auto_20200727_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='meta_description',
            field=models.TextField(null=True, verbose_name='Meta Description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='page_title',
            field=models.CharField(max_length=155, null=True, verbose_name='Page title'),
        ),
    ]