# Generated by Django 3.0.5 on 2020-07-01 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0103_auto_20200701_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='additional_parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Category', verbose_name='double_category'),
        ),
    ]
