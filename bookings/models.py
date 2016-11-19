from __future__ import unicode_literals

from django.db import models
from assets.models import Asset
from django.conf import settings
from django.utils import timezone

# class Booking_OLD(models.Model):
#
#     class Meta:
#         app_label="bookings"
#
#     booking_id = models.AutoField(primary_key=True)
#     asset_ID = models.ForeignKey(Asset,on_delete=models.CASCADE, related_name="asset_booked")
#     requested_by_user_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="requested_by")
#     slot_owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     start_date = models.DateField(blank=False)
#     end_date = models.DateField(blank=False)
#     is_confirmed = models.BooleanField(default=False)
#     deposit_paid = models.BooleanField(default=False)
#     date_created = models.DateTimeField(default=timezone.now)
#     date_confirmed = models.DateTimeField(blank=True, null=True)
#
#     def __unicode__(self):
#         return "%s | from %s to %s | userId: %s" % (self.asset_ID.asset_display_name, self.start_date, self.end_date, self.requested_by_user_ID.id)

class Booking(models.Model):

    class Meta:
        app_label="bookings"

    booking_id = models.AutoField(primary_key=True)
    asset_ID = models.ForeignKey(Asset,on_delete=models.CASCADE, related_name="asset_booked")
    requested_by_user_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="requested_by")
    deposit_paid = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)



    def __unicode__(self):
        return "%s | for %s | requested by userId: %s " % (self.booking_id, self.asset_ID.asset_display_name, self.requested_by_user_ID.id)

class BookingDetail(models.Model):

    class Meta:
        app_label="bookings"

    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE,related_name='bookingdetails')
    slot_owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_date = models.DateField(blank=False)
    is_confirmed = models.BooleanField(default=False)
    date_confirmed = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "%s | for %s | owned by userId: %s" % (self.booking_id, self.booking_date, self.slot_owner_id.id)