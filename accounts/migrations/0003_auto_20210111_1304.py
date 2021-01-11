# Generated by Django 3.1.4 on 2021-01-11 13:04

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210111_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_image',
            field=models.ImageField(blank=True, default=accounts.models.get_default_profile_image, max_length=255, null=True, upload_to=accounts.models.get_profile_image_filepath),
        ),
    ]
