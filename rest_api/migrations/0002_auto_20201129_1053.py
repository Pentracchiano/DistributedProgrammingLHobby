# Generated by Django 3.1.3 on 2020-11-29 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='elo',
            field=models.PositiveSmallIntegerField(default=1000),
        ),
    ]
