# Generated by Django 2.0.6 on 2019-03-11 09:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20190310_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 3, 11, 9, 14, 41, 723680, tzinfo=utc)),
        ),
    ]
