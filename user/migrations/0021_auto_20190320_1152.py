# Generated by Django 2.0.6 on 2019-03-20 11:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0020_auto_20190318_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 3, 20, 11, 52, 4, 331513, tzinfo=utc)),
        ),
    ]