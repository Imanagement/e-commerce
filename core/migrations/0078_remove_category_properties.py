# Generated by Django 3.0.5 on 2020-06-11 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0077_property_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='properties',
        ),
    ]
