# Generated by Django 3.0.5 on 2020-06-23 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0085_auto_20200623_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='ip',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='session',
            field=models.CharField(max_length=50),
        ),
    ]
