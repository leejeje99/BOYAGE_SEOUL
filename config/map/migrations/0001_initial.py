# Generated by Django 3.1 on 2020-08-27 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('lat', models.CharField(max_length=25)),
                ('lng', models.CharField(max_length=25)),
                ('gu', models.CharField(default=1, max_length=25)),
            ],
        ),
    ]
