# Generated by Django 3.0.5 on 2020-05-14 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200514_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='test',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
