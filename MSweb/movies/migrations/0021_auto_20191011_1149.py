# Generated by Django 2.2.5 on 2019-10-11 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0020_auto_20191011_1148'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='movielistitem',
            unique_together={('movie_list', 'movie_title', 'slug')},
        ),
    ]
