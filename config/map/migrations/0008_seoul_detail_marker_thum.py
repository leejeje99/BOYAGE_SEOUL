# Generated by Django 3.1 on 2020-09-07 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0007_seoul_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='seoul_detail',
            name='marker_thum',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
