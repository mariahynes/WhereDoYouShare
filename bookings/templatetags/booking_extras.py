from django import template
import datetime
from bookings.models import BookingDetail

register = template.Library()

@register.simple_tag
def get_total_for_approval(asset_id, user_id):

    #the number of requests awaiting this owner approval for the given asset_id
    total = 0

    all = BookingDetail.objects.all().filter(slot_owner_id_id=user_id, booking_id__asset_ID=asset_id,
                                       booking_date__gt=datetime.date.today(), is_pending=True)

    total = all.count()

    return total

@register.simple_tag
def get_total_for_confirmation(asset_id, user_id):

    # the number of requests approved/denied by an Owner
    # that are waiting for original Requestor to approve
    total = 0

    requests_to_confirm = BookingDetail.objects.all().filter(booking_id__requested_by_user_ID=user_id,
                                                             booking_date__gt=datetime.date.today(), is_pending=False,
                                                             booking_id__asset_ID=asset_id, is_confirmed=False)

    total = requests_to_confirm.count()

    return total

@register.simple_tag
def get_num_total_pending(asset_id, user_id):

    # the number of requests that are pending for this user
    total = 0

    requests_pending = BookingDetail.objects.all().filter(booking_id__requested_by_user_ID=user_id,
                                                          booking_date__gt=datetime.date.today(),
                                                          booking_id__asset_ID=asset_id, is_pending=True)

    total = requests_pending.count()

    return total

@register.filter
def get_total_days_requested(owner_and_dates):

    total_days_requested = 0

    for item in owner_and_dates:
        total_days_requested += item.days_requested

    return total_days_requested

@register.filter
def get_total_days_available(owner_and_dates):

    total_days_available = 0

    for item in owner_and_dates:

        for available_date in item.date_span_available_detail:
            total_days_available += 1

    return total_days_available

@register.filter
def get_total_owner_slots(owner_and_dates):

    total_owner_slots = 0

    for item in owner_and_dates:

            total_owner_slots += 1

    return total_owner_slots

@register.filter
def get_total_days_unavailable(owner_and_dates):

    total_days_unavailable = 0

    for item in owner_and_dates:

        for unavailable_date in item.date_span_unavailable_detail:
            total_days_unavailable += 1

    return total_days_unavailable


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
def get_booking_date_status(booking_pk):

    # this function takes the pk of the individual dated record
    # and NOT the booking ref
    item = BookingDetail.objects.get(pk=booking_pk)

    if item.is_confirmed:
        the_status = "Confirmed"
    elif item.is_pending:
        the_status = "Pending"
    elif item.is_approved:
        the_status = "Approved"
    elif item.is_denied:
        the_status = "Denied"
    else:
        the_status = "---"

    return the_status

@register.simple_tag
def get_booking_asset_name(booking_id):
    a_name = BookingDetail.objects.all().filter(booking_id=booking_id).order_by("-booking_date")[0]
    asset = a_name.booking_id.asset_ID.asset_display_name

    return asset

@register.simple_tag
def get_booking_status(booking_id):

    if is_booking_confirmed(booking_id):

        return "Confirmed"

    elif is_booking_pending(booking_id):

        return "Still Pending"

    else:

        # the record is no longer in a pending state and is not yet confirmed
        # so that means it must be approved/denied

        num_approved = get_approved_count(booking_id)
        num_denied = get_denied_count(booking_id)
        total_requested = get_total_days_in_booking(booking_id)

        if num_approved == total_requested:
            return "Yes"
        elif num_denied == total_requested:
            return "No"
        else:
            return "%s of %s days" % (num_approved, total_requested)


@register.simple_tag
def get_approved_count(booking_id):

    # count the number of approved records for the booking id
    num_approved_records = BookingDetail.objects.all().filter(booking_id=booking_id, is_approved=True).count()
    return num_approved_records

@register.simple_tag
def get_denied_count(booking_id):

    # count the number of denied records for the booking id
    num_denied_records = BookingDetail.objects.all().filter(booking_id=booking_id, is_denied=True).count()
    return num_denied_records

@register.simple_tag
def is_booking_pending(booking_id):

    # count the number of confirmed records for the booking id
    num_pending_records = BookingDetail.objects.all().filter(booking_id=booking_id, is_pending=True).count()
    # count the number of days in the booking
    days_in_booking = get_total_days_in_booking(booking_id)

    # if they match, then the booking is confirmed
    if num_pending_records==days_in_booking:

        return True

    else:

        return False

@register.simple_tag
def is_booking_confirmed(booking_id):

    # count the number of confirmed records for the booking id
    num_confirmed_records = BookingDetail.objects.all().filter(booking_id=booking_id, is_confirmed=True).count()
    # count the number of days in the booking
    days_in_booking = get_total_days_in_booking(booking_id)

    # if they match, then the booking is confirmed
    if num_confirmed_records==days_in_booking:

        return True

    else:

        return False

@register.simple_tag
def get_confirmed_date(booking_id):

    if is_booking_confirmed(booking_id):

        # get the confirmed date from any of the records - they will all be the same
        # because all records in a booking can only be confirmed at the same time
        a_record = BookingDetail.objects.all().filter(booking_id=booking_id, is_confirmed=True)[0]
        confirmed_date = a_record.date_confirmed
        return confirmed_date

    else:

        return ""




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

@register.simple_tag
def get_total_days_in_booking(booking_id):

    a = BookingDetail.objects.all().filter(booking_id=booking_id)
    total_days = a.count()

    return total_days