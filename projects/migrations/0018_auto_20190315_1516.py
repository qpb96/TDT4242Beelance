# Generated by Django 2.0.6 on 2019-03-15 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_project_requested_promotion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='requested_promotion',
            new_name='has_requested_promotion',
        ),
    ]
