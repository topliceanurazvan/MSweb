# Generated by Django 2.2.5 on 2019-10-12 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0028_auto_20191012_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movielist',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
