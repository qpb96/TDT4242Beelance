# Generated by Django 2.0.6 on 2019-03-08 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20190308_2304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='writtenBy',
            new_name='author',
        ),
    ]
