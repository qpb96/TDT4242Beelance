# Generated by Django 2.0.6 on 2019-03-16 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_promotionpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotionpayment',
            name='fee',
            field=models.FloatField(default=0),
        ),
    ]
