# Generated by Django 3.0.5 on 2020-06-03 17:14

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_remove_product_main_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='main_image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=''),
        ),
    ]