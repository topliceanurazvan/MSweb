# Generated by Django 2.2.5 on 2019-10-11 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0024_auto_20191011_1151'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='movielistitem',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='movierating',
            unique_together=set(),
        ),
    ]