from django import template
import datetime
from bookings.models import BookingDetail

register = template.Library()

@register.filter
def get_total_pending(pending_requests,asset_id):

    total = 0

    for booking in pending_requests:
        if asset_id == asset_id:
            total += 1

    return total

@register.simple_tag
def get_booking_start_date(booking_id):

    a_date = BookingDetail.objects.all().filter(booking_id=booking_id).order_by("booking_date")[0]
    min_date = a_date.booking_date.strftime("%d %b %Y")

    return min_date

@register.simple_tag
def get_booking_end_date(booking_id):
    a_date = BookingDetail.objects.all().filter(booking_id=booking_id).order_by("-booking_date")[0]
    max_date = a_date.booking_date

    # add one day on (because departure will be the NEXT day)
    max_date = max_date + datetime.timedelta(days=1)
    max_date = max_date.strftime("%d %b %Y")

    return max_date

@register.simple_tag
def get_booking_asset_name(booking_id):
    a_name = BookingDetail.objects.all().filter(booking_id=booking_id).order_by("-booking_date")[0]
    asset = a_name.booking_id.asset_ID.asset_display_name

    return asset

@register.simple_tag
def is_booking_confirmed(booking_id):

    no = BookingDetail.objects.all().filter(booking_id=booking_id, is_confirmed=False)
    no_count = no.count()
    yes = BookingDetail.objects.all().filter(booking_id=booking_id, is_confirmed=True)
    yes_count = yes.count()

    if no_count > 0 and yes_count > 0:

        return "Partially (%s of %s days)" % (yes_count, yes_count+no_count)

    elif no_count > 0:

        return "No"

    else:
         return "Yes"

@register.simple_tag
def get_booking_slot_owner(booking_id):
    bd = BookingDetail.objects.all().filter(booking_id=booking_id).order_by("slot_owner_id")

    owner = set()
    space = ""
    for item in bd:
        the_name = "%s %s" % (item.slot_owner_id.first_name, item.slot_owner_id.last_name)
        owner.add(the_name)

    owner_string = ""
    for person in owner:
        owner_string = "%s %s | " % (owner_string,person)

    # remove last |
    owner_string = owner_string[:-2]

    return owner_string