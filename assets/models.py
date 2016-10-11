from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone

class Asset(models.Model):

    class Meta:
        app_label = "assets"

    asset_display_name = models.CharField(max_length=255, blank=False)
    asset_type = models.ForeignKey('AssetType', on_delete=models.CASCADE)
    sharing_with_other_owners = models.BooleanField (default=0)
    sharing_start_date = models.DateField(blank=False)
    slot_duration_unit = models.ForeignKey('DurationType', on_delete=models.CASCADE)
    number_of_slot_units = models.IntegerField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Asset_User_Mapping')

    def __unicode__(self):
        return self.asset_display_name

class Asset_User_Mapping(models.Model):

    class Meta:
        app_label = "assets"

    user_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    asset_ID = models.ForeignKey('Asset', on_delete=models.CASCADE)
    is_owner = models.BooleanField(blank=False)
    position_in_rotation = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    is_activated = models.BooleanField(blank=False)
    date_activated = models.DateTimeField(blank=True, null=True)
    invited_by = models.CharField(max_length=50, blank=True, null=True)

    def activate_user_mapping(self):
        self.date_activated = timezone.now()
        self.save()

    def __unicode__(self):
        return "%s %s | %s " %(self.user_ID.first_name, self.user_ID.last_name, self.asset_ID)

class AssetType(models.Model):

    class Meta:
        app_label = "assets"

    asset_type = models.CharField(max_length=255)

    def __unicode__(self):
        return self.asset_type

class DurationType(models.Model):

    class Meta:
        app_label = "assets"

    duration_type = models.CharField(max_length=255)

    def __unicode__(self):
        return self.duration_type