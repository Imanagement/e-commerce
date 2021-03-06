# Generated by Django 3.0.5 on 2020-07-27 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0146_auto_20200725_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='on_stock',
        ),
        migrations.AddField(
            model_name='product',
            name='not_in_stock',
            field=models.BooleanField(default=False, help_text='Если помечено галочкой, наличие товара будет отображаться "На складах компании" ', verbose_name='Нет на складе'),
        ),
    ]
