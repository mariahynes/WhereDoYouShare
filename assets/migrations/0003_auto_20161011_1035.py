# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-11 09:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20161010_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset_user_mapping',
            name='invited_by',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='asset_user_mapping',
            name='user_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asset_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
