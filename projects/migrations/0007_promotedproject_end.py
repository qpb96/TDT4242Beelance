# Generated by Django 2.0.6 on 2019-03-01 15:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20190301_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotedproject',
            name='end',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 3, 1, 15, 2, 38, 3954)),
        ),
    ]
