# Generated by Django 3.1.1 on 2020-12-29 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0016_auto_20201222_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='description',
            field=models.URLField(blank=True, max_length=100),
        ),
    ]
