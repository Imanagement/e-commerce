# Generated by Django 3.0.6 on 2020-10-06 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0192_testclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='extraoption',
            name='categories',
            field=models.ManyToManyField(to='core.Category', verbose_name='Категории дополнительной опции'),
        ),
    ]
