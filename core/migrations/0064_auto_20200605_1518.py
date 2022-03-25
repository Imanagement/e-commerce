# Generated by Django 3.0.5 on 2020-06-05 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0063_auto_20200604_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name='propertyvalue',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Product'),
        ),
        migrations.AlterField(
            model_name='propertyvalue',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Property'),
        ),
    ]
