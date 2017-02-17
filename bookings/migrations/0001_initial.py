# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-11 09:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0003_auto_20161011_1035'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.IntegerField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_confirmed', models.BooleanField(default=False)),
                ('deposit_paid', models.BooleanField(default=False)),
                ('asset_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asset_booked', to='assets.Asset')),
                ('requested_by_user_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_by', to=settings.AUTH_USER_MODEL)),
                ('slot_owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
