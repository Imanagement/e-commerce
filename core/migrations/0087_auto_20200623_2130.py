# Generated by Django 3.0.5 on 2020-06-23 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0086_auto_20200623_2117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productreview',
            old_name='user',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='productreview',
            old_name='ip',
            new_name='customer_ip',
        ),
        migrations.RenameField(
            model_name='productreview',
            old_name='session',
            new_name='customer_session',
        ),
    ]
