# Generated by Django 3.0.5 on 2020-05-28 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20200528_1313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='has_child',
            new_name='has_child_category',
        ),
    ]
