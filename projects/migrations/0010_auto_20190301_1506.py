# Generated by Django 2.0.6 on 2019-03-01 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_auto_20190301_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotedproject',
            name='start',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
