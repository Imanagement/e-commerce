# Generated by Django 3.0.5 on 2020-06-25 10:00

from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0091_mpttcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('has_child_category', models.BooleanField(default=True)),
                ('custom_slug', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, max_length=55, null=True, unique=True)),
                ('category_level', models.IntegerField(blank=True, null=True)),
                ('image', imagekit.models.fields.ProcessedImageField(upload_to='')),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Test_Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='category_level',
        ),
        migrations.RemoveField(
            model_name='category',
            name='has_child_category',
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent_id',
        ),
        migrations.AddField(
            model_name='category',
            name='level',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='lft',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.Category'),
        ),
        migrations.AddField(
            model_name='category',
            name='rght',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='MpttCategory',
        ),
    ]