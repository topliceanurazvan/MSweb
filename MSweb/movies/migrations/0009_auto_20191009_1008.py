# Generated by Django 2.2.5 on 2019-10-09 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_auto_20191009_1004'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movielist',
            old_name='slug_list',
            new_name='slug',
        ),
        migrations.RenameField(
            model_name='movielistitem',
            old_name='slug_item',
            new_name='slug',
        ),
    ]
