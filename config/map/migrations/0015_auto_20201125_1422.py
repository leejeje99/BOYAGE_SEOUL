# Generated by Django 3.1 on 2020-11-25 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0014_auto_20201125_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seoul_detail',
            name='name',
            field=models.CharField(max_length=125),
        ),
    ]
