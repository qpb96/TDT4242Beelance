# Generated by Django 2.0.6 on 2018-10-30 20:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.TextField(blank=True, max_length=50)),
                ('phone_number', models.TextField(blank=True, max_length=50)),
                ('street_address', models.TextField(blank=True, max_length=50)),
                ('city', models.TextField(blank=True, max_length=50)),
                ('state', models.TextField(blank=True, max_length=50)),
                ('postal_code', models.TextField(blank=True, max_length=50)),
                ('country', models.TextField(blank=True, max_length=50)),
                ('categories', models.ManyToManyField(related_name='competance_categories', to='projects.ProjectCategory')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
