# Generated by Django 3.0.5 on 2020-06-03 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_product_main_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='test',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
