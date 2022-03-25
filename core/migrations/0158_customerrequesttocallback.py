# Generated by Django 3.0.5 on 2020-08-15 16:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0157_delete_customerrequesttocallback'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerRequestToCallBack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField()),
                ('ip', models.CharField(max_length=32)),
                ('customer_called_back', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Зарегистрированный покупатель')),
            ],
        ),
    ]