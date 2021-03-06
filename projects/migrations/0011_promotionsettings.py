# Generated by Django 2.0.6 on 2019-03-08 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20190301_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pool_size', models.IntegerField(default=20)),
                ('display_amount', models.IntegerField(default=0)),
                ('promotion_fee', models.IntegerField(default=0.0)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
