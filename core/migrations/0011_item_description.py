# Generated by Django 3.0.5 on 2020-05-14 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20200514_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
