# Generated by Django 3.0.5 on 2020-06-24 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0089_mttptestclass'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mttptestclass',
            options={'verbose_name': 'Test', 'verbose_name_plural': 'Tests'},
        ),
        migrations.RenameField(
            model_name='mttptestclass',
            old_name='parent_id',
            new_name='parent',
        ),
    ]
