# Generated by Django 4.2 on 2024-02-07 11:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_project_created_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='issue',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
