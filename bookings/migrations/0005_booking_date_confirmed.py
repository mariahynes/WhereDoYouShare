# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-19 16:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_auto_20161015_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='date_confirmed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]