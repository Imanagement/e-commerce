# Generated by Django 3.0.5 on 2020-07-01 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0106_auto_20200701_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='additional_parent',
        ),
        migrations.AddField(
            model_name='category',
            name='additional_parents',
            field=models.ManyToManyField(related_name='_category_additional_parents_+', to='core.Category', verbose_name='repeated_categories'),
        ),
    ]
