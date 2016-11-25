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


import datetime

@login_required(login_url='/login/')
def my_bookings(request):

    my_id = request.user

    # this is all FUTURE bookings for every asset (>=today)
    my_future_bookings = BookingDetail.objects.all().filter(booking_id__requested_by_user_ID=my_id,
                                                            booking_date__gte=datetime.date.today()).order_by(
        "-booking_date")

    # this is all PAST bookings for every asset (<today)
    my_past_bookings = BookingDetail.objects.all().filter(booking_id__requested_by_user_ID=my_id,
                                                            booking_date__lt =datetime.date.today()).order_by(
        "-booking_date")

    # need a unique sets of booking ids, so populate sets
    booking_ids_future = set()
    booking_ids_past = set()

    if my_future_bookings:
        for item in my_future_bookings:
            booking_ids_future.add(item.booking_id_id)

    if my_past_bookings:
        for item in my_past_bookings:
            booking_ids_past.add(item.booking_id_id)

    # in future Set want to sort by earliest to latest
    future_date_and_booking_id = []
    for booking_id in booking_ids_future:
        the_date = get_booking_start_date(booking_id)
        # have to convert to date so that it can be sorted as a date and not as a string
        the_date = datetime.datetime.strptime(the_date, "%d %b %Y")
        the_date = the_date.strftime("%Y%m%d")
        future_date_and_booking_id.append((the_date, booking_id))

    # and sort by the date before sending to the template
    future_date_and_booking_id = sorted(future_date_and_booking_id, key=lambda tup: tup[0])

    num_bookings_future = booking_ids_future.__len__()

    # in past Set want to sort by latest to earliest
    past_date_and_booking_id = []
    for booking_id in booking_ids_past:
        the_date = get_booking_start_date(booking_id)
        # have to convert to date so that it can be sorted as a date and not as a string
        the_date = datetime.datetime.strptime(the_date, "%d %b %Y")
        the_date = the_date.strftime("%Y%m%d")
        past_date_and_booking_id.append((the_date, booking_id))

    # and sort by the date before sending to the template
    past_date_and_booking_id = sorted(past_date_and_booking_id, key=lambda tup: tup[0])

    num_bookings_past = booking_ids_past.__len__()

    # send list of assets for this user
    assets = Asset_User_Mapping.objects.all().filter(user_ID=request.user)

    return render(request, "bookings.html", {"assets": assets, "future_bookings": future_date_and_booking_id,
                                             "num_bookings_future": num_bookings_future,
                                             "past_bookings": past_date_and_booking_id,
                                             "num_bookings_past": num_bookings_past})


@login_required(login_url='/login/')
def all_future_asset_bookings(request, asset_id, **kwargs):

    # this function returns all the future bookings for an asset
    # can provide optional kwarg with the user id if to return bookings for a particular user

    the_asset = get_object_or_404(Asset, pk=asset_id)

    errors = []

    if kwargs.has_key("for_this_user"):
        this_user_only = kwargs['for_this_user']
    else:
        this_user_only = False

    my_id = request.user
    if check_user_linked_to_asset(my_id, asset_id):

        # optional userID
        if not this_user_only:
            all_bookings = get_future_bookings(asset_id)
            all_bookings = Booking.objects.all().filter(asset_ID=the_asset).filter(start_date__gt=datetime.date.today())

        else:
            all_bookings = get_future_bookings(asset_id, user_id=my_id)
            all_bookings = Booking.objects.all().filter(asset_ID=the_asset, requested_by_user_ID=my_id,
                                                                                   start_date__gt=datetime.date.today())

    else:
        the_asset = []
        all_bookings = []
        errors.append("You are not authorised to view this Booking page")

    return render(request, "all_bookings.html", {"asset": the_asset, "all_bookings": all_bookings, "errors": errors})

@login_required(login_url='/login/')
def booking_detail(request, booking_id):

    the_booking = get_object_or_404(Booking, pk=booking_id)
    errors = []
    asset = []
    booking_detail = []

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

    return render(request, "booking_detail.html",{"booking":the_booking,"booking_detail": booking_detail, "asset":asset,"errors":errors})


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

                print "the Detail: %s" % item.date_span_available_detail
                for available_date in item.date_span_available_detail:
                    booking_date = available_date

                    # check if the owner is booking one of their own dates
                    # if so, then set immediately to is_confirmed == True
                    if owner_id == my_id:

                        new_record = BookingDetail(booking_date=booking_date,
                                                   slot_owner_id_id=owner_id,
                                                   booking_id_id=new_id,
                                                   is_confirmed=True,
                                                   date_confirmed=datetime.datetime.now())
                    else:

                        new_record = BookingDetail(booking_date=booking_date,
                                                   slot_owner_id_id=owner_id,
                                                   booking_id_id=new_id,
                                                   is_pending=True,
                                                   date_pending=datetime.datetime.now())


                    new_record.save()

            # messages.success(request, "New Booking created, thanks")
            return redirect(reverse('booking_detail', args={new_booking.pk}))

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



def get_future_bookings(asset_id, **kwargs):

    for_user = False

    if kwargs.has_key("user_id"):
        requested_by = kwargs['user_id']
        for_user = True

    if for_user:
        future_bookings = BookingDetail.objects.all().filter(booking_id__requested_by_user_ID=requested_by,
                                                             booking_id__asset_ID=asset_id,
                                                         booking_date__gt=datetime.date.today()).order_by(
                                                                "booking_date")

    # need a unique set of future booking ids
    booking_ids = set()
    if future_bookings:
        for item in future_bookings:
            booking_ids.add(item.booking_id_id)

    num_bookings = booking_ids.__len__()

    # would like to order by booking date but once booking_ids go into the set, the set is ordered by booking_id
    # so here, populate new tuple with booking_id and earliest start_date per booking
    date_and_booking_id = []
    for booking_id in booking_ids:
        the_date = get_booking_start_date(booking_id)
        # have to convert to date so that it can be sorted as a date and not as a string
        the_date = datetime.datetime.strptime(the_date, "%d %b %Y")
        the_date = the_date.strftime("%Y%m%d")
        date_and_booking_id.append((the_date, booking_id))

    # and sort by the date before sending to the template
    date_and_booking_id = sorted(date_and_booking_id, key=lambda tup: tup[0])

    assets = Asset_User_Mapping.objects.all().filter(user_ID=request.user)