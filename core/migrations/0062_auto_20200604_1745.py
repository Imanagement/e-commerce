# Generated by Django 3.0.5 on 2020-06-04 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0061_auto_20200604_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertyvalue',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='property_value', related_query_name='property_value_qs', to='core.Product'),
        ),
        migrations.AlterField(
            model_name='propertyvalue',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property', related_query_name='property_qs', to='core.Property'),
        ),
    ]