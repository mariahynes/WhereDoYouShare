from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from assets.models import Asset, Asset_User_Mapping
from bookings.templatetags.booking_extras import get_booking_start_date
from .models import Booking, BookingDetail
from .forms import BookingForm
from myfunctions import get_owners_and_dates
from home.myAuth import check_user_linked_to_asset
import datetime
from django.utils import timezone
from django.db.models import Q

@login_required(login_url='/login/')
def my_bookings(request):

    my_id = request.user

    # this is all FUTURE bookings for every asset (>=today)
    # returned in a set of booking_date and booking ref
    my_future_bookings = get_bookings(user_id=my_id,time_period="future")
    num_bookings_future = len(my_future_bookings)

    # this is all PAST bookings for every asset (<today)
    # returned in a set of booking_date and booking ref
    my_past_bookings = get_bookings(user_id=my_id, time_period="past")
    num_bookings_past = len(my_past_bookings)

    # send list of assets for this user
    assets = Asset_User_Mapping.objects.all().filter(user_ID=request.user)

    return render(request, "bookings.html", {"assets": assets, "future_bookings": my_future_bookings,
                                             "num_bookings_future": num_bookings_future,
                                             "past_bookings": my_past_bookings,
                                             "num_bookings_past": num_bookings_past})


@login_required(login_url='/login/')
def all_future_asset_bookings(request, asset_id, user_id=0):

    # this function returns all the future bookings for an asset
    # can provide optional arg with the user id which will return bookings for a particular user only

    the_asset = get_object_or_404(Asset, pk=asset_id)
    this_user_only = False
    errors = []

    if request.user.id == int(user_id):
        this_user_only = True

    my_id = request.user
    if check_user_linked_to_asset(my_id, asset_id):

        # optional userID
        if this_user_only:

            all_bookings = get_bookings(asset_id=asset_id, user_id=request.user.id, time_period="future")

        else:

            all_bookings = get_bookings(asset_id=asset_id, time_period="future")

    else:
        the_asset = []
        all_bookings = []
        errors.append("You are not authorised to view this Booking page")

    return render(request, "all_bookings.html",
                  {"asset": the_asset, "bookings": all_bookings, "errors": errors, "return_page_user": user_id})

@login_required(login_url='/login/')
def all_bookings(request, asset_id="", status = "", time_period = "", user_id=""):

    # this function returns all the bookings refs in the Booking Table
    # for an asset (optional)
    # for a given status (optional) e.g.pending, approved, confirmed, denied, or all
    # for a given user (optional)

    errors = []
    the_asset = []
    all_bookings = []
    my_id = request.user
    user_is_linked = False
    time_range = "all"

    if asset_id != "":
        the_asset = get_object_or_404(Asset, pk=asset_id)

        if check_user_linked_to_asset(my_id, asset_id):
            user_is_linked = True

    this_user_only = False
    if request.user.id == int(user_id):
        this_user_only = True


    if len(time_period) > 0:
        if time_period == "future":
            time_range = time_period
        elif time_period == "past":
            time_range == time_period

    if asset_id != 0:

        if user_is_linked == True:
            # then the query is for bookings for a particular asset
            # check optional userID
            if this_user_only:
                # only bookings for this user (for this asset)
                all_bookings = get_bookings(asset_id=asset_id, user_id=my_id, time_period=time_range)

            else:
                # bookings belonging to any user (for this asset)
                all_bookings = get_bookings(asset_id=asset_id,time_period=time_range)

        else:
            errors.append("You are not authorised to view this asset")

    else:
        # this is not bookings for one particular asset, but bookings for all assets
        # but only return bookings from assets that the user is allowed to view

        if this_user_only:
            # only bookings for this user (for all assets)
            all_bookings = get_bookings(user_id=my_id,time_period=time_range)

        else:
            # bookings belonging to any user (for all assets)
            all_bookings = get_bookings(time_period=time_range)
            # filter this result to return only the bookings from assets the user is allowed to view
            for ref in all_bookings:
                print "ref in all bookings: %s" % ref

    # now check if the status is required
    if status == "pending":
        pass
    elif status == "approved":
        pass
    elif status == "confirmed":
        pass
    elif status == "denied":
        pass
    else:
        pass

    return render(request, "all_bookings.html",
                  {"asset": the_asset, "bookings": all_bookings, "errors": errors, "return_page_user": user_id})

@login_required(login_url='/login/')
def booking_detail(request, booking_id, new=""):

    the_booking = get_object_or_404(Booking, pk=booking_id)
    errors = []
    asset = []
    booking_detail = []
    if new != "new":
        new = ""

    # get the asset id (from the booking)
    asset_id = the_booking.asset_ID_id

    # anyone linked to the Asset can view the booking
    # but only the requestor can edit the booking
    my_id = request.user
    if check_user_linked_to_asset(my_id,asset_id):

        asset = Asset.objects.get(pk=asset_id)
        booking_detail = BookingDetail.objects.select_related().filter(booking_id_id=booking_id).order_by("booking_date")

    else:
        errors.append("You are not authorised to view this booking")

    return render(request, "booking_detail.html",{"booking":the_booking,"booking_detail": booking_detail, "asset":asset,"errors":errors, "new":new})


@login_required(login_url='/login/')
def make_a_booking(request, asset_id):

    the_asset = get_object_or_404(Asset, pk=asset_id)
    errors = []
    owner_date_object = []
    total_days_requested = 0
    booking_form = []

    my_id = request.user
    if check_user_linked_to_asset(my_id, asset_id):
        user_ok = True
    else:
        user_ok = False
        errors.append("You are not authorised to view this page")

    if request.method == "POST":
        new_booking_form = BookingForm(request.POST)
        if new_booking_form.is_valid():

            # save it in memory while getting the addition info need to save it to the database
            new_booking = new_booking_form.save(False)
            # get additional info
            new_booking.asset_ID_id = asset_id
            new_booking.requested_by_user_ID = request.user
            # then save
            new_booking.save()

            # now, using the new_booking.pk, save each of the dates in BookingDetail
            new_id = new_booking.pk

            start_date = request.POST['start_date']
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = request.POST['end_date']
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            owner_date_object = get_owners_and_dates(asset_id, start_date, end_date)

            print "object count is %s" % len(owner_date_object)

            for item in owner_date_object:

                owner_id = item.owner_id
                print "ownerId: %s" % owner_id
                print "current user: %s" % request.user.id

                print "the Detail: %s" % item.date_span_available_detail
                for available_date in item.date_span_available_detail:
                    booking_date = available_date

                    # check if the owner is booking one of their own dates
                    # if so, then set immediately to is_confirmed == True
                    if owner_id == request.user.id:

                        new_record = BookingDetail(booking_date=booking_date,
                                                   slot_owner_id_id=owner_id,
                                                   booking_id_id=new_id,
                                                   is_approved=True,
                                                   date_approved=timezone.now())
                    else:

                        new_record = BookingDetail(booking_date=booking_date,
                                                   slot_owner_id_id=owner_id,
                                                   booking_id_id=new_id,
                                                   is_pending=True)


                    new_record.save()
                    new = "new"
            # messages.success(request, "New Booking created, thanks")
            return redirect(reverse('booking_detail', kwargs={"booking_id":new_booking.pk, "new":new}))

    else:

        #request.method is GET,
        #check which stage of get
        if 'start_date' in request.GET:
            new_booking_form = BookingForm(request.GET)
            if new_booking_form.is_valid():
                start_date = request.GET['start_date']
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

                if 'end_date' in request.GET:
                    end_date = request.GET['end_date']
                    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

                if end_date.toordinal() - start_date.toordinal() < 0:
                    errors.append('Your end date is earlier than your start date - please correct!')

                    new_booking_form = BookingForm(request.GET)

                elif end_date.toordinal() == start_date.toordinal():
                    errors.append('Your start and end dates are the same - please correct!')

                    new_booking_form = BookingForm(request.GET)

                else:
                    # dates are fine (unless I programme more validation) so now continue with
                    # displaying the ownership for the date range!
                    print "Data to function: %s %s %s" % (asset_id, start_date, end_date)
                    owner_date_object = get_owners_and_dates(asset_id, start_date, end_date)

                    new_booking_form = BookingForm(request.GET)
            else:

                new_booking_form = BookingForm(request.GET)
        else:
            # this is first time so just display the form
            new_booking_form = BookingForm()

    args = {
        'booking_form': new_booking_form,
        'the_asset': the_asset,
        'errors': errors,
        'owner_date_object': owner_date_object,
        'user_ok': user_ok,
    }

    args.update(csrf(request))

    return render(request, "new_booking.html", args)



def get_bookings(**kwargs):

    # by default, this query if sent NO kwargs will return a set of dates and ids for
    # all future dates for all assets for all users
    # using the optional parameters can return a set of dates and ids for
    # all dates OR all past OR all futures dates, one or all users, one or all assets

    requested_by = ""
    this_asset = ""
    time_period = ""

    if kwargs.has_key("user_id"):
        requested_by = kwargs['user_id']

    if kwargs.has_key("asset_id"):
        this_asset = kwargs['asset_id']

    # time period expected: 'all', 'past', or 'future'
    if kwargs.has_key("time_period"):
        time_period = kwargs['time_period']

    # from http://stackoverflow.com/questions/852414/how-to-dynamically-compose-an-or-query-filter-in-django
    query_params = Q()

    if requested_by != "":
        query_params.add(Q(booking_id__requested_by_user_ID=requested_by), Q.AND)

    if this_asset != "":
        query_params.add(Q(booking_id__asset_ID=this_asset), Q.AND)

    if time_period == "future":
        query_params.add(Q(booking_date__gt=datetime.date.today()),Q.AND)

    if time_period == "past":
        query_params.add(Q(booking_date__lte=datetime.date.today()), Q.AND)

    future_bookings = BookingDetail.objects.all().filter(query_params).order_by("booking_date")

    # need a unique set of future booking ids
    booking_ids = set()
    if future_bookings:
        for item in future_bookings:
            booking_ids.add(item.booking_id_id)

    # need to order by booking date but once booking_ids go into the set, the set is ordered by booking_id
    # so here, populate new tuple with booking_id and earliest start_date per booking
    date_and_booking_id = []
    for booking_id in booking_ids:
        the_date = get_booking_start_date(booking_id)
        # have to convert to ordinal so that it can be sorted
        the_date.toordinal()
        date_and_booking_id.append((the_date, booking_id))

    # and sort by the date before sending to the template
    date_and_booking_id = sorted(date_and_booking_id, key=lambda tup: tup[0])

    return date_and_booking_id