
from django import template
from django.core.urlresolvers import reverse
from django.conf import settings
from assets.models import Asset, Asset_User_Mapping
register = template.Library()
import datetime
import calendar
from bookings.templatetags.booking_extras import get_owner_name_for_user_id_and_asset
from home.myAuth import check_if_user_is_an_owner
from bookings.myfunctions import get_owners_and_dates

@register.filter
def my_asset_count(asset_user_mapping):
    total_assets = asset_user_mapping.objects.count(requested_by_User_ID=settings.AUTH_USER_MODEL)

    return total_assets

@register.simple_tag
def get_total_asset_members(asset_id):

    total_members = 0
    all_users = Asset_User_Mapping.objects.all().filter(asset_ID_id=asset_id, is_owner=False)

    total_members = all_users.count()


    return total_members

@register.simple_tag
def get_total_asset_owners(asset_id):

    total_owners = 0
    all_owners = Asset_User_Mapping.objects.all().filter(asset_ID_id=asset_id, is_owner=True)

    total_owners = all_owners.count()


    return total_owners

@register.simple_tag
def get_slot_unit_desc(asset_id):

    asset_record = Asset.objects.get(pk=asset_id)
    the_slot_unit = asset_record.slot_duration_unit.duration_type

    return the_slot_unit


@register.simple_tag
def get_num_slots(asset_id):
    asset_record = Asset.objects.get(pk=asset_id)
    num_slots = asset_record.number_of_slot_units

    return num_slots

@register.simple_tag
def get_slot_start_desc(asset_id):

    asset_record = Asset.objects.get(pk=asset_id)
    first_date = asset_record.sharing_start_date

    slot_unit = get_slot_unit_desc(asset_id)

    if slot_unit == "Week":
        # find out what DAY of the week is first_date
        the_desc = calendar.day_name[first_date.weekday()]

    elif slot_unit == "Month":
        # return the number date
        the_desc = first_date.day

    else:
        # return empty string because it's a single-owned asset
        the_desc = ""

    return the_desc

@register.simple_tag
def get_slot_desc_summary(asset_id):

    num_slots = get_num_slots(asset_id)
    start_desc = get_slot_start_desc(asset_id)
    unit_desc = get_slot_unit_desc(asset_id)

    if unit_desc.lower() == "week":
        start_desc = "%s %s" % ("a",start_desc)

    if unit_desc.lower() == "month":
        # get number suffix
        start_desc = "%s%s" % (start_desc,get_ordinal(start_desc))
        start_desc = "%s %s" % ("the", start_desc)

    if unit_desc.lower() != "one owner":

        if num_slots < 2:

            desc_summary = "Every 2%s %s starting on %s " % (get_ordinal(2),unit_desc.lower(), start_desc)

        else:

            desc_summary = "Every %s %s%s starting on %s" % (num_slots, unit_desc.lower(),"s",start_desc)

    else:

        desc_summary = ""

    return desc_summary


@register.simple_tag
def get_asset_invitor_for_display(asset_id, user_id):

    # this returns nothing if the user_id is the owner_id or if
    # there is only one owner of the asset

    my_linked_owner = get_owner_name_for_user_id_and_asset(asset_id,user_id)

    # just check if this person is an owner of this asset
    if check_if_user_is_an_owner(user_id, asset_id):

        my_linked_owner = ""

    # and check that there is more than one owner
    if get_total_asset_owners(asset_id) == 1:
        my_linked_owner = ""

    return my_linked_owner

@register.simple_tag
def get_asset_invitor(asset_id, user_id, first_name_only = False):

    # this returns the name of the owner
    my_linked_owner = get_owner_name_for_user_id_and_asset(asset_id,user_id,first_name_only=first_name_only)

    return my_linked_owner


@register.simple_tag
def get_next_slot_start(asset_id, owner_id):

    # check that there is more than one owner
    if get_total_asset_owners(asset_id) == 1:

        return ""

    current_date = datetime.date.today()
    next_date = current_date + datetime.timedelta(days=1)
    slot_owner_id = 0
    start_of_slot = current_date

    while slot_owner_id != owner_id:

        owner_date_obj = get_owners_and_dates(asset_id,current_date,next_date)

        for item in owner_date_obj:
            slot_owner_id = item.owner_id
            start_of_slot = item.start_for_owner
            # update dates for next time in loop
            current_date = next_date
            next_date = current_date + datetime.timedelta(days=1)

    print "owner id the same: %s and %s: " % (slot_owner_id,owner_id)
    print "owner id start: %s: " % start_of_slot

    the_day = start_of_slot.strftime("%d")
    fancy_day = get_ordinal(int(the_day))
    formatted_date = start_of_slot.strftime("%b %Y")
    fancy_date = "%s%s %s" % (int(the_day), fancy_day, formatted_date)

    return fancy_date




def get_ordinal(the_num):

    suffix = ['st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th',
              'th', 'th', 'th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'st']

    the_num -= 1

    return suffix[the_num]
