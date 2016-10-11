from __future__ import unicode_literals

from django.db import models
from assets.models import Asset
from django.conf import settings
from django.utils import timezone

class Booking(models.Model):

    class Meta:
        app_label="bookings"

    booking_id = models.AutoField(primary_key=True)
    asset_ID = models.ForeignKey(Asset,on_delete=models.CASCADE, related_name="asset_booked")
    requested_by_user_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="requested_by")
    slot_owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    is_confirmed = models.BooleanField(default=False)
    deposit_paid = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s | from %s to %s | userId: %s" % (self.asset_ID.asset_display_name, self.start_date, self.end_date, self.requested_by_user_ID.id)



