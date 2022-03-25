# Generated by Django 3.0.5 on 2020-06-04 12:33

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_auto_20200603_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='main_image',
            field=imagekit.models.fields.ProcessedImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(upload_to=''),
        ),
    ]
