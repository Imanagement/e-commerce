# Generated by Django 3.0.5 on 2020-07-01 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0100_auto_20200630_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='show_on_the_homepage_at_the_footer',
            field=models.BooleanField(default=False),
        ),
    ]
