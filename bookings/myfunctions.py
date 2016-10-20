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

    # ensure the dates are python dates (may not be needed when coming from database)
    dateformat = '%Y-%m-%d'
    start_date = request_start
    end_date = request_end

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

    # get the number of slots from static start date to requested start date
    # in order to work out the number of slots since static start date
    delta = start_date - static_start_date
    num_duration_periods_from_static_to_start = delta.days / 7
    num_slot_periods_in_static_to_start = num_duration_periods_from_static_to_start / num_slots
    print "%s is the number of %s since static start date" % (num_duration_periods_from_static_to_start, slot_duration)
    print "%s is number of slots since static start date" % num_slot_periods_in_static_to_start

    # then which slot in the rotation order is being requested
    remainder_of_mod = divmod(num_slot_periods_in_static_to_start, len(sort_order_of_owners))
    slot_order_on_requested_start_date = remainder_of_mod[1] + 1
    slot_owner_on_requested_start_date = sort_order_of_owners.get(slot_order_on_requested_start_date)
    print "%s is slot order on the requested start date" % slot_order_on_requested_start_date
    print "%s is the ID of the owner on the requested start date" % slot_owner_on_requested_start_date

    # requested start date is in someone's slot - get the start and end date of that slot
    slot_start_for_start_date = get_start_slot_date(static_start_date, start_date, num_days_per_period, dateformat)
    slot_end_for_start_date = get_end_slot_date(slot_start_for_start_date,num_days_per_period)
    print "%s is start of slot with requested start date" % slot_start_for_start_date
    print "%s is end of slot with requested start date" % slot_end_for_start_date

    # now work out if only one owner is affected by the requested date range
    # or more than one owner
    # store Owner ID and slot start and slot end dates in object to return

    # if the number of days from requested end date to end of the slot is >=0
    # then there is no need to move into the next slot i.e. only one owner should be returned

    delta = slot_end_for_start_date - end_date

    if delta.days >= 0:

        print "Only one owner to return"

        owners_and_dates.append(slot_owner_on_requested_start_date,slot_start_for_start_date, slot_end_for_start_date)

    else:

        print "More than one owner to return"

        delta = slot_end_for_start_date - start_date
        num_days_slot_1 = delta.days
        print "%s days required from owner slot 1: " % num_days_slot_1, slot_owner_on_requested_start_date

        days_to_cover = requested_num_days - num_days_slot_1
        print "%s days left to cover" % days_to_cover

        end_of_previous_slot = slot_end_for_start_date

        # use this to check rows/items to return
        slots_affected = 1

        previous_slot_order = slot_order_on_requested_start_date

        while days_to_cover > 0:

            # get date info for next slot
            next_slot_start_date = end_of_previous_slot
            next_slot_end = get_end_slot_date(next_slot_start_date, num_days_per_period)

            # get sort order of next slot
            if (previous_slot_order + 1) > len(sort_order_of_owners):
                next_slot_order = 1
            else:
                next_slot_order = previous_slot_order + 1

            # get slot owner of next slot
            next_slot_owner = sort_order_of_owners.get(next_slot_order)

            # increment
            slots_affected += 1

            # check if remainder days is more than one duration period
            if days_to_cover > num_days_per_period:

                # this is not the last time in loop because there are more days to cover
                # reset to remainder for next time in loop
                days_to_cover = days_to_cover - num_days_per_period
                end_of_previous_slot = next_slot_end
                previous_slot_order = next_slot_order

                print "%s is owner ORDER" % next_slot_order
                print "%s days required from next owner with ID: %s" % (num_days_per_period, next_slot_owner)
                print "%s is start of next slot" % next_slot_start_date
                print "%s is end of next slot" % next_slot_end
                print "%s days still to cover" % days_to_cover

            else:

                # finally, we have come to the end because remaining days to cover is less than one duration period
                delta = end_date - next_slot_start_date
                days_of_current_slot = delta.days
                print "%s days required until end of the booking" % days_of_current_slot
                print "%s days required from next (final) owner with ID:" % next_slot_owner
                print "%s is start of next (final) slot" % next_slot_start_date
                print "%s is end of next (final) slot" % next_slot_end

                # make sure to set to zero to end the loop
                days_to_cover = 0

    return "slots affected: %s" % slots_affected



def get_start_slot_date(slot_static_start_date, requested_start_date, days_step, dateformat):

    from_date = slot_static_start_date.toordinal()
    to_date = requested_start_date.toordinal()

    owner_slot_start_date = from_date

    for j in range(from_date, to_date,days_step):

        if owner_slot_start_date < to_date:

            owner_slot_start_date = j

    start_slot_date = datetime.date.fromordinal(owner_slot_start_date)

    return start_slot_date



def get_end_slot_date(start_date, days_step):

    end_slot_date = start_date + datetime.timedelta(days_step)

    return end_slot_date









