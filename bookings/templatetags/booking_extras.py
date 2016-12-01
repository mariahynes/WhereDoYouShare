from django import template
import datetime
from assets.models import Asset_User_Mapping
from bookings.models import BookingDetail
from home.myAuth import check_user_linked_to_owner

register = template.Library()

@register.simple_tag
def get_total_for_approval(asset_id, user_id, **kwargs):
    # FUTURE approval for an OWNER
    # this function returns either the number of dates OR the number of booking refs
    # awaiting this owner approval for the given asset_id
    # if kwarg 'num_bookings' == True, then it's the total bookings returned,
    # otherwise it's the number of individual dates returned

    return_bookings = False

    if kwargs.has_key("num_bookings"):
        return_bookings = kwargs['num_bookings']


    # check if the given user_id is an owner
    # only OWNERS can approve, so the user_id here is checked against the slot owner field
    all_dates = BookingDetail.objects.all().filter(slot_owner_id_id=user_id, booking_id__asset_ID=asset_id,
                                                   booking_date__gt=datetime.date.today(), is_pending=True)


    if return_bookings:
        ref_set = set()
        # get the unique booking refs
        for the_date in all_dates:
            ref_set.add(the_date.booking_id_id)

        total = len(ref_set)

    else:

        total = all_dates.count()

    return total

@register.simple_tag
def get_total_for_approval_linked(asset_id, user_id, **kwargs):
    # FUTURE approval for a MEMBER (members don't approve,
    # but they should know about approvals to which they are linked)
    # this function returns either the number of dates OR the number of booking refs
    # that are awaiting approval BUT only returns a value if this user_id is linked to the owner
    # if kwarg 'num_bookings' == True, then it's the total bookings returned,
    # otherwise it's the number of individual dates returned

    return_bookings = False
    total = 0

    if kwargs.has_key("num_bookings"):
        return_bookings = kwargs['num_bookings']

    # first just get all the future pending bookings for the assest
    all_pending_dates = BookingDetail.objects.all().filter(booking_id__asset_ID=asset_id,
                                                   booking_date__gt=datetime.date.today(), is_pending=True)

    if return_bookings:
        # need the booking ids only
        ref_set = set()

        # check the owner/member link for each of the records returned
        for item in all_pending_dates:
            the_owner_id = item.slot_owner_id_id
            is_linked = check_user_linked_to_owner(user_id, the_owner_id, asset_id)
            if is_linked:
                ref_set.add(item.booking_id_id)

        total = len(ref_set)

    else:
        # need the count of dates
        # check the owner/member link for each of the records returned
        for item in all_pending_dates:
            the_owner_id = item.slot_owner_id_id
            print "owner %s" % the_owner_id
            is_linked = check_user_linked_to_owner(user_id, the_owner_id, asset_id)
            print "is linked %s" % is_linked
            if is_linked:
                total += 1
                print "total: %s" % total

    return total

@register.simple_tag
def get_owner_name_for_user_id_and_asset(asset_id, user_id, **kwargs):

    # this returns the name of the owner who invited this user
    # remember this COULD return the logged-in user's own name
    # if they are an owner

    get_first_name = False

    if kwargs.has_key("first_name_only"):
        get_first_name = kwargs['first_name_only']

    the_owner = Asset_User_Mapping.objects.get(user_ID_id=user_id,asset_ID_id=asset_id)

    owner_first_name = the_owner.inviter.first_name
    owner_last_name = the_owner.inviter.last_name

    if get_first_name:

        return owner_first_name

    else:

        return "%s %s" % (owner_first_name, owner_last_name)

@register.simple_tag
def get_total_for_confirmation(asset_id, user_id, **kwargs):
    # FUTURE confirmation
    # this function returns either the number of dates OR the number of booking refs
    # that are waiting for original Requestor to approve
    # if kwarg 'num_bookings' == True, then it's the total bookings returned,
    # otherwise it's the number of individual dates returned
    # if a booking is ready to be confirmed there can be NO pending records

    return_bookings = False

    if kwargs.has_key("num_bookings"):
        return_bookings = kwargs['num_bookings']

    # the user_id here is checked against the requested by user field from Booking table
    all_booking_dates = BookingDetail.objects.all().filter(booking_id__requested_by_user_ID=user_id,
                                                             booking_date__gt=datetime.date.today(), is_pending=False,
                                                             booking_id__asset_ID=asset_id, is_confirmed=False)

    if return_bookings:
        ref_set = set()
        # get the unique booking refs
        for item in all_booking_dates:
            # only add to the set if there are no other pending dates in the booking ref
            # could be some pending if the user is the owner and has approved only their own dates
            # or if multiple owners have to approve
            ref = item.booking_id
            if not is_booking_pending(ref):
                ref_set.add(item.booking_id_id)

        total = len(ref_set)

    else:

        total = all_booking_dates.count()

    return total

@register.simple_tag
def get_total_confirmed_bookings(asset_id, user_id):
    # # FUTURE confirmed
    # this function returns the number of booking refs
    # that are fully confirmed for this user

    total_count = 0

    # the user_id here is checked against the requested by user field from Booking table
    all_bookings = BookingDetail.objects.all().filter(booking_id__requested_by_user_ID=user_id,
                                                             booking_date__gt=datetime.date.today(),
                                                             booking_id__asset_ID=asset_id, is_confirmed=True)


    # make a set in order to get individual booking refs
    ref_set = set()
    # get the unique booking refs
    for item in all_bookings:
        ref_set.add(item.booking_id_id)

    for ref in ref_set:
        if is_booking_confirmed(ref):
            total_count += 1

    return total_count

@register.simple_tag
def get_total_bookings(asset_id):
    # FUTURE bookings
    # this function returns the number of booking refs
    # that for the Asset

    total_count = 0

    # the user_id here is checked against the requested by user field from Booking table
    all_bookings = BookingDetail.objects.all().filter( booking_date__gt=datetime.date.today(),
                                                             booking_id__asset_ID=asset_id)


    # make a set in order to get individual booking refs
    ref_set = set()

    # get the unique booking refs
    for item in all_bookings:
        ref_set.add(item.booking_id_id)

    total_count = len(ref_set)

    return total_count

@register.simple_tag
def get_total_bookings_past(asset_id):
    # PAST bookings
    # this function returns the number of booking refs
    # for the Asset

    total_count = 0

    all_bookings = BookingDetail.objects.all().filter( booking_date__lte=datetime.date.today(),
                                                             booking_id__asset_ID=asset_id)


    # make a set in order to get individual booking refs
    ref_set = set()

    # get the unique booking refs
    for item in all_bookings:
        ref_set.add(item.booking_id_id)

    total_count = len(ref_set)

    return total_count

@register.simple_tag
def get_total_pending(asset_id, user_id, **kwargs):
    # FUTURE pending
    # this function returns either the number of dates OR the number of booking refs
    # that are pending for this user
    # if kwarg 'num_bookings' == True, then it's the total bookings returned,
    # otherwise it's the number of individual dates returned

    return_bookings = False

    if kwargs.has_key("num_bookings"):
        return_bookings = kwargs['num_bookings']

    all_dates = BookingDetail.objects.all().filter(booking_id__requested_by_user_ID=user_id,
                                                          booking_date__gt=datetime.date.today(),
                                                          booking_id__asset_ID=asset_id, is_pending=True)

    if return_bookings:
        ref_set = set()
        # get the unique booking refs
        for the_date in all_dates:
            ref_set.add(the_date.booking_id_id)

        total = len(ref_set)

    else:

        total = all_dates.count()

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

    print "BookingID: %s" % booking_id
    a_date = BookingDetail.objects.all().filter(booking_id=booking_id).order_by("booking_date")[0]
    min_date = a_date.booking_date

    return min_date

@register.simple_tag
def get_last_date_in_booking(booking_id):

    print "BookingID: %s" % booking_id
    a_date = BookingDetail.objects.all().filter(booking_id=booking_id).order_by("-booking_date")[0]
    last_date = a_date.booking_date

    return last_date

@register.simple_tag
def get_booking_end_date(booking_id):

    # for display purposes, this takes last booked date and adds '1' to be able to say
    # from/until
    # for exact last date use get_last_date_in_booking function
    a_date = BookingDetail.objects.all().filter(booking_id=booking_id).order_by("-booking_date")[0]
    max_date = a_date.booking_date

    max_date = max_date + datetime.timedelta(days=1)

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
def get_booking_date(booking_pk):

    # this function takes the pk of the individual dated record
    # and NOT the booking ref
    item = BookingDetail.objects.get(pk=booking_pk)

    the_date = item.booking_date

    return the_date

@register.simple_tag
def get_booking_date_owner(booking_pk):

    # this function takes the pk of the individual dated record
    # and NOT the booking ref
    item = BookingDetail.objects.get(pk=booking_pk)

    the_name = "%s %s" % (item.slot_owner_id.first_name, item.slot_owner_id.last_name)

    return the_name

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

        return "Pending"

    else:

        # the booking is no longer pending state and is not yet confirmed
        # so that means it must be approved/denied
        # either way, this is considered to be "awaiting confirmation"
        # because next step can only be carried out by the Requestor

        # I had all this fancy stuff but not needed, just the status is all I want here
        # num_approved = get_approved_count(booking_id)
        # num_denied = get_denied_count(booking_id)
        # total_requested = get_total_days_in_booking(booking_id)
        #
        # if num_approved == total_requested:
        #     return "Awaiting Confirmation"
        # elif num_denied == total_requested:
        #     return "Awaiting Confirmation"
        # else:
        #     return "Awaiting Confirmation %s of %s days approved" % (num_approved, total_requested)

        return "Awaiting Confirmation"

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

    # count the number of pending records for the booking id
    # if there are ANY pending dates, then the booking is considered pending
    # could be some approved, some denied and some pending (depending on whether a few owners have to approve)

    num_pending_records = BookingDetail.objects.all().filter(booking_id=booking_id, is_pending=True).count()

    if num_pending_records > 0:

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

    # for a booking ref, there could be more than one Owner
    # this function places the Owners in a set so that they only appear once in the output
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
def get_booking_requestor(booking_id,**kwargs):

    # there will only be one Requestor per booking
    # but could be many booking dates in that Booking,
    # so only return the first item in the object
    # return the first_name second_name by defauly
    # return the id if "return_id" in kwargs
    return_id = False

    if kwargs.has_key("return_id"):
        return_id = kwargs['return_id']

    bd = BookingDetail.objects.select_related().filter(booking_id=booking_id)[0]

    if return_id:
        the_name = bd.booking_id.requested_by_user_ID_id
    else:
        the_name = "%s %s" % (bd.booking_id.requested_by_user_ID.first_name, bd.booking_id.requested_by_user_ID.last_name)


    return the_name

@register.simple_tag
def get_total_days_in_booking(booking_id):

    a = BookingDetail.objects.all().filter(booking_id=booking_id)
    total_days = a.count()

    return total_days

@register.simple_tag
def booking_has_consec_dates(booking_id):

    start_date = get_booking_start_date(booking_id)
    last_date = get_last_date_in_booking(booking_id)
    num_dates = get_total_days_in_booking(booking_id)

    expected_last_date = start_date + datetime.timedelta(days=num_dates-1)

    if expected_last_date == last_date:

        return True

    else:

        return False
