# Generated by Django 3.0.5 on 2020-08-17 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0158_customerrequesttocallback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerrequesttocallback',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]
