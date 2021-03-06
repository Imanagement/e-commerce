# Generated by Django 3.0.6 on 2020-09-29 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0185_auto_20200929_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='slug',
            field=models.SlugField(default='', help_text='Slug - текст в адресе страницы после tehnomall.md например slug для контакт: /kontakti ', max_length=30, verbose_name='Slug страницы'),
            preserve_default=False,
        ),
    ]
