# Generated by Django 3.1 on 2020-09-02 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0005_auto_20200902_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='formainlat',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AddField(
            model_name='place',
            name='formainlng',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
