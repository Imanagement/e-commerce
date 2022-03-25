# Generated by Django 3.0.5 on 2020-06-24 11:53

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0088_product_sku'),
    ]

    operations = [
        migrations.CreateModel(
            name='MttpTestClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('has_child_category', models.BooleanField(default=True)),
                ('custom_slug', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, max_length=55, null=True, unique=True)),
                ('category_level', models.IntegerField(blank=True, null=True)),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent_id', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.MttpTestClass')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
    ]
