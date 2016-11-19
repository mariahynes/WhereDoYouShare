from assets.models import Asset, Asset_User_Mapping
from accounts.models import User
from bookings.models import Booking, BookingDetail
import datetime
import monthdelta

def get_owners_and_dates_WEEK_CALC_ONLY(asset_ID, request_start, request_end):

    # define the owners_and_dates class that will be populated and returned

    class Owners_And_Dates(object):

        slots = 0

        def __init__(self, owner_id, first_name, last_name, start_for_owner, end_for_owner, days_requested):
            self.owner_id = owner_id
            self.start_for_owner = start_for_owner
            self.end_for_owner = end_for_owner
            self.first_name = first_name
            self.last_name = last_name
            self.days_requested = days_requested
            Owners_And_Dates.slots += 1

        def owner_display_name(self):
            return "%s %s" % (self.first_name, self.last_name)

        def numberOfSlots(self):
            return Owners_And_Dates.slots

        def __repr__(self):
            return "Owner is: %s | Start Date: %s | End Date: %s" % (self.owner_id, self.owner_display_name, self.start_for_owner, self.end_for_owner)

        def __str__(self):
            return "Owner is: %s | Start Date: %s | End Date: %s" % (self.owner_id, self.start_for_owner, self.end_for_owner)

    # empty object
    owners_and_dates_list = []
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
        slot_duration_days = 28
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
        slots_affected = 1
        delta = slot_end_for_start_date - start_date
        num_days_slot_1 = delta.days

        o = User.objects.get(id=slot_owner_on_requested_start_date)
        o_and_d = Owners_And_Dates(slot_owner_on_requested_start_date, o.first_name, o.last_name,
                                   slot_start_for_start_date, slot_end_for_start_date, num_days_slot_1)
        owners_and_dates_list.append(o_and_d)

    else:

        print "More than one owner to return"
        # first slot details
        delta = slot_end_for_start_date - start_date
        num_days_slot_1 = delta.days

        o = User.objects.get(id=slot_owner_on_requested_start_date)
        o_and_d = Owners_And_Dates(slot_owner_on_requested_start_date, o.first_name, o.last_name, slot_start_for_start_date,
                                   slot_end_for_start_date,num_days_slot_1)

        owners_and_dates_list.append(o_and_d)


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

                o = User.objects.get(id=next_slot_owner)
                o_and_d = Owners_And_Dates(next_slot_owner, o.first_name, o.last_name, next_slot_start_date,
                                           next_slot_end,num_days_per_period)

                owners_and_dates_list.append(o_and_d)

            else:

                # finally, we have come to the end because remaining days to cover is less than one duration period
                delta = end_date - next_slot_start_date
                days_of_current_slot = delta.days
                print "%s is owner ORDER" % next_slot_order
                print "%s days required until end of the booking" % days_of_current_slot
                print "%s days required from next (final) owner with ID: %s" % (days_of_current_slot,next_slot_owner)
                print "%s is start of next (final) slot" % next_slot_start_date
                print "%s is end of next (final) slot" % next_slot_end

                o = User.objects.get(id=next_slot_owner)
                o_and_d = Owners_And_Dates(next_slot_owner, o.first_name, o.last_name, next_slot_start_date,
                                           next_slot_end,days_of_current_slot)

                owners_and_dates_list.append(o_and_d)

                # make sure to set to zero to end the loop
                days_to_cover = 0
                print "%s days still to cover" % days_to_cover

    # return "owners and dates: %s | slots affected: %s" % (owners_and_dates_list,slots_affected)
    return owners_and_dates_list

# revised this function to include Monthly Calcs
def get_owners_and_dates(asset_ID, request_start, request_end):

    # define the owners_and_dates class that will be populated and returned

    class Owners_And_Dates(object):

        slots = 0

        def __init__(self, owner_id, first_name, last_name, start_for_owner, end_for_owner, start_requested, end_requested, days_requested, days_available):
            self.owner_id = owner_id
            self.start_for_owner = start_for_owner
            self.end_for_owner = end_for_owner
            self.start_requested = start_requested
            self.end_requested = end_requested
            self.first_name = first_name
            self.last_name = last_name
            self.days_requested = days_requested
            self.days_available = days_available
            Owners_And_Dates.slots += 1

        def owner_display_name(self):
            return "%s %s" % (self.first_name, self.last_name)

        def numberOfSlots(self):
            return Owners_And_Dates.slots

        def __repr__(self):
            return "Owner is: %s | Start Date: %s | End Date: %s" % (self.owner_id, self.owner_display_name, self.start_for_owner, self.end_for_owner)

        def __str__(self):
            return "Owner is: %s | Start Date: %s | End Date: %s" % (self.owner_id, self.start_for_owner, self.end_for_owner)

    # empty object
    owners_and_dates_list = []
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

    # don't continue if the requested start date is on or before the static start date!
    if request_start <= static_start_date:
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
    elif str(slot_duration) == "Month":
        slot_duration_days = 30 # can't use a set number here for months
    else:
        slot_duration = 1

    # calculate number of days in the owner-duration period
    num_days_per_period = slot_duration_days * num_slots

    if str(slot_duration) == "Week":

        # get the number of slots from static start date to requested start date
        # in order to work out the number of slots since static start date
        delta = start_date - static_start_date
        num_duration_periods_from_static_to_start = delta.days / slot_duration_days
        num_slot_periods_in_static_to_start = num_duration_periods_from_static_to_start / num_slots
        print "%s is the number of %s since static start date" % (num_duration_periods_from_static_to_start, slot_duration)
        print "%s is number of slots since static start date" % num_slot_periods_in_static_to_start

    elif str(slot_duration) == "Month":

        # get the number of months from static start date to requested start date
        # this will be the number of slots since static start date
        num_months = monthdelta.monthmod(static_start_date,start_date)
        num_duration_periods_from_static_to_start = num_months[0].months
        num_slot_periods_in_static_to_start = int(num_duration_periods_from_static_to_start) / num_slots
        print "%s is the number of %s since static start date" % (num_duration_periods_from_static_to_start, slot_duration)
        print "%s is number of slots since static start date" % num_slot_periods_in_static_to_start
        print "%s is the days remaining" % num_months[1].days

    # then which slot in the rotation order is being requested
    remainder_of_mod = divmod(num_slot_periods_in_static_to_start, len(sort_order_of_owners))
    slot_order_on_requested_start_date = remainder_of_mod[1] + 1
    slot_owner_on_requested_start_date = sort_order_of_owners.get(slot_order_on_requested_start_date)
    print "%s is slot order on the requested start date" % slot_order_on_requested_start_date
    print "%s is the ID of the owner on the requested start date" % slot_owner_on_requested_start_date

    # requested start date is in someone's slot - get the start and end date of that slot
    if str(slot_duration) == "Week":
        slot_start_for_start_date = get_start_slot_date(static_start_date, start_date, num_days_per_period, dateformat)
        slot_end_for_start_date = get_end_slot_date(slot_start_for_start_date,num_days_per_period)

    elif str(slot_duration) == "Month":
        # start date will simply be day of static start day with month and year of requested start date!
        slot_start_for_start_date = datetime.date(start_date.year, start_date.month, static_start_date.day)
        # slot end will be the same date plus <num_slots> later
        slot_end_for_start_date = slot_start_for_start_date + monthdelta.monthdelta(num_slots)

    print "%s is start of slot with requested start date" % slot_start_for_start_date
    print "%s is end of slot with requested start date" % slot_end_for_start_date

    # now work out if only one owner is affected by the requested date range
    # or more than one owner
    # store Owner ID and slot start and slot end dates in object to return

    # first slot details
    delta = slot_end_for_start_date - start_date
    num_days_slot_1 = delta.days

    # check Booking table to find out the number of days available for the range
    num_days_available = check_availability(asset_ID, start_date, slot_end_for_start_date)
    o = User.objects.get(id=slot_owner_on_requested_start_date)
    o_and_d = Owners_And_Dates(slot_owner_on_requested_start_date, o.first_name, o.last_name,
                               slot_start_for_start_date, slot_end_for_start_date, start_date, slot_end_for_start_date,
                               num_days_slot_1, num_days_available)
    owners_and_dates_list.append(o_and_d)

    # if the number of days from requested end date to end of the slot is >=0
    # then there is no need to move into the next slot i.e. only one owner should be returned
    delta = slot_end_for_start_date - end_date

    if delta.days >= 0:
        print delta.days
        print "Only one owner to return"
        slots_affected = 1

    else:

        print "More than one owner to return"

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

            if str(slot_duration) == "Week":
                next_slot_end = get_end_slot_date(next_slot_start_date, num_days_per_period)
            elif str(slot_duration) == "Month":
                next_slot_end = next_slot_start_date + monthdelta.monthdelta(num_slots)


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
            # works for weeks (always 7 days), but for months, need to calculate the ACTUAL number of days
            # in the next period (this will vary with different length months)

            if str(slot_duration) == "Month":
                num_days_in_next_period = next_slot_end.toordinal() - next_slot_start_date.toordinal()
                # store in this variable for ease of code
                num_days_per_period = num_days_in_next_period

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

                num_days_available = check_availability(asset_ID, next_slot_start_date, next_slot_end)
                o = User.objects.get(id=next_slot_owner)
                o_and_d = Owners_And_Dates(next_slot_owner, o.first_name, o.last_name, next_slot_start_date,
                                           next_slot_end,next_slot_start_date,next_slot_end,num_days_per_period,num_days_available)

                owners_and_dates_list.append(o_and_d)

            else:

                # finally, we have come to the end because remaining days to cover is less than one duration period
                delta = end_date - next_slot_start_date
                days_of_current_slot = delta.days
                print "%s is owner ORDER" % next_slot_order
                print "%s days required until end of the booking" % days_of_current_slot
                print "%s days required from next (final) owner with ID: %s" % (days_of_current_slot,next_slot_owner)
                print "%s is start of next (final) slot" % next_slot_start_date
                print "%s is end of next (final) slot" % next_slot_end

                num_days_available = check_availability(asset_ID, next_slot_start_date, end_date)
                o = User.objects.get(id=next_slot_owner)
                o_and_d = Owners_And_Dates(next_slot_owner, o.first_name, o.last_name, next_slot_start_date,
                                           next_slot_end,next_slot_start_date, end_date, days_of_current_slot,num_days_available)

                owners_and_dates_list.append(o_and_d)

                # make sure to set to zero to end the loop
                days_to_cover = 0
                print "%s days still to cover" % days_to_cover

    # return "owners and dates: %s | slots affected: %s" % (owners_and_dates_list,slots_affected)
    return owners_and_dates_list

def get_start_slot_date(slot_static_start_date, requested_start_date, days_step, dateformat):

    from_date = slot_static_start_date.toordinal()
    to_date = requested_start_date.toordinal()

    owner_slot_start_date = from_date

    for j in range(from_date, to_date, days_step):

        if owner_slot_start_date < to_date:

            owner_slot_start_date = j

    start_slot_date = datetime.date.fromordinal(owner_slot_start_date)

    return start_slot_date



def get_end_slot_date(start_date, days_step):

    end_slot_date = start_date + datetime.timedelta(days_step)

    return end_slot_date


def check_availability(asset_id,start_date, end_date):

    # check if ach date in the span between start_date and end_date is in the bookingdetail table for this asset_id
    # could be pending or confirmed
    # this function (at the moment) just returns number of nights available (i.e. NOT pending or confirmed)

    count_available = 0

    return count_available




# def get_owner_display_name(owner_id):
#
#
#     settings.AUTH_USER_MODEL
#     my_bookings = Booking.objects.all().filter(requested_by_user_ID=my_id)
#     return






