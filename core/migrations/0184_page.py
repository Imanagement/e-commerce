# Generated by Django 3.0.6 on 2020-09-29 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0183_auto_20200926_0721'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='Название страницы')),
                ('page_title', models.CharField(max_length=155, verbose_name='Title страницы')),
                ('meta_description', models.TextField(verbose_name='Meta description страницы')),
            ],
        ),
    ]
