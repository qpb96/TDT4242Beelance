# Generated by Django 2.0.6 on 2019-03-10 18:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20190310_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 3, 10, 18, 54, 10, 622044, tzinfo=utc)),
        ),
    ]
