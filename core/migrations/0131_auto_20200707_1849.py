# Generated by Django 3.0.5 on 2020-07-07 15:49

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0130_auto_20200707_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Описание'),
        ),
    ]
