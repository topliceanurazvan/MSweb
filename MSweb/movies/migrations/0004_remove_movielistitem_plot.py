# Generated by Django 2.2.5 on 2019-10-08 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_movielist_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movielistitem',
            name='plot',
        ),
    ]
