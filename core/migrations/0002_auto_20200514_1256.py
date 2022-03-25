# Generated by Django 3.0.5 on 2020-05-14 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='brand',
            field=models.CharField(choices=[('AP', 'Apple'), ('SM', 'Samsung'), ('XM', 'Xiaomi'), ('DL', 'Dell'), ('TB', 'Toshiba'), ('NB', 'NoBrand')], default='NB', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('C', 'Computer'), ('M', 'Mobile'), ('L', 'Laptop'), ('NC', 'NoCategory')], default='NC', max_length=2),
            preserve_default=False,
        ),
    ]
