# Generated by Django 2.2.5 on 2019-10-09 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_movielistitem_plot'),
    ]

    operations = [
        migrations.AddField(
            model_name='movielistitem',
            name='rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
