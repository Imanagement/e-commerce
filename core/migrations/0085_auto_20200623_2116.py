# Generated by Django 3.0.5 on 2020-06-23 18:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0084_productreview_publish_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='ip',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='productreview',
            name='session',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='productreview',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='productreview',
            name='publish_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
