# Generated by Django 3.0.5 on 2020-06-03 18:38

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0057_auto_20200603_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='test',
        ),
        migrations.AlterField(
            model_name='product',
            name='main_image',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to=''),
        ),
    ]
