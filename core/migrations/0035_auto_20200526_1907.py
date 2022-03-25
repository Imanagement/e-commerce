# Generated by Django 3.0.5 on 2020-05-26 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20200526_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='published',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.CreateModel(
            name='ProductView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=50)),
                ('session', models.CharField(max_length=50)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Product')),
            ],
            options={
                'verbose_name': 'ProductView',
                'verbose_name_plural': 'ProductViews',
            },
        ),
    ]
