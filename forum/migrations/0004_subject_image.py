# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-09 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_auto_20161207_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='forum_images'),
        ),
    ]
