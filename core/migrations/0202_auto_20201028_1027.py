# Generated by Django 3.0.6 on 2020-10-28 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0201_auto_20201022_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerrequesttocallback',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customerrequesttocallback',
            name='name',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
