# Generated by Django 2.0.6 on 2019-03-08 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20190308_1422'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promotionsettings',
            old_name='duration',
            new_name='duration_in_days',
        ),
    ]
