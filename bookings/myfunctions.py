from assets.models import Asset, Asset_User_Mapping
import arrow
import datetime

def hello_world():
    return "Hi!"

def get_owners_and_dates(asset_ID, request_start, request_end):

    # empty object
    owners_and_dates = []
    # empty dictionary
    sort_order_of_owners = {}

    # get the asset in question
    the_asset = Asset.objects.get(pk=asset_ID)

    # extract the variables needed for later
    static_start_date = the_asset.sharing_start_date
    slot_duration = the_asset.slot_duration_unit
    num_slots = the_asset.number_of_slot_units

    # don't continue if no slots entered (will get divide by zero error)
    if num_slots == 0:
        return []

    # populate dictionary of the sort order and owners
    the_asset_mapping = Asset_User_Mapping.objects.all().filter(asset_ID=asset_ID, is_owner=True).order_by("position_in_rotation")

    if the_asset_mapping.count() == 0:
        return []

    for mapping in the_asset_mapping:

        sort_order_of_owners[mapping.position_in_rotation] = mapping.user_ID_id


    # ensire the dates are python dates (may not be needed when coming from database)
    dateformat = '%Y-%m-%d'
    start_date = datetime.datetime.strptime(request_start,dateformat)
    end_date = datetime.datetime.strptime(request_end, dateformat)

    # calculate number of days requested (i.e. number of nights)
    requested_num_days = end_date.toordinal() - start_date.toordinal()
    print "%s nights" % requested_num_days

    if str(slot_duration) == "Week":
        slot_duration_days = 7
    elif str(slot_duration) == "Day":
        slot_duration_days = 1
    else:
        slot_duration_days = 99

    # calculate number of days in the owner-duration period
    num_days_per_period = slot_duration_days * num_slots

    # requested start date is in someone's slot - get the start and end date of that slot
    slot_start_for_start_date = get_start_slot_date(static_start_date, start_date, num_days_per_period, dateformat)
    slot_end_for_start_date = get_end_slot_date(slot_start_for_start_date,num_days_per_period)

    print "%s is start of slot with requested start date" % slot_start_for_start_date
    print "%s is end of slot with requested start date" % slot_end_for_start_date

    # get the number of slots from static start date to requested start date
    # in order to work out which slot in the rotation order is being requested







    return slot_end_for_start_date



def get_start_slot_date(slot_static_start_date, requested_start_date, days_step, dateformat):

    from_date = slot_static_start_date.toordinal()
    to_date = requested_start_date.toordinal()

    owner_slot_start_date = from_date

    for j in range(from_date, to_date,days_step):

        if owner_slot_start_date < to_date:

            owner_slot_start_date = j

    start_slot_date = datetime.date.fromordinal(owner_slot_start_date).strftime('%Y-%m-%d')
    start_slot_date = datetime.datetime.strptime(start_slot_date,dateformat)

    return start_slot_date



def get_end_slot_date(start_date, days_step):

    end_slot_date = start_date + datetime.timedelta(days_step)

    return end_slot_date









