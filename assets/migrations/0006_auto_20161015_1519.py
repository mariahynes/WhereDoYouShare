# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-15 14:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0005_asset_user_mapping_inviter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='asset_user_mapping',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
