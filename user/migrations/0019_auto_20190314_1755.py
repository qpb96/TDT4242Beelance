# Generated by Django 2.0.6 on 2019-03-14 16:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_auto_20190312_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 3, 14, 16, 55, 46, 967784, tzinfo=utc)),
        ),
    ]
