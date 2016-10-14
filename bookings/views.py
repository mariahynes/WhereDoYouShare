from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from assets.models import Asset, Asset_User_Mapping
from .models import Booking
from accounts.models import User
from django.conf import settings
import datetime

@login_required(login_url='/login/')
def bookings(request):
    my_id = request.user
    my_bookings = Booking.objects.filter(requested_by_user_ID=my_id)
    return render(request, "bookings.html", {"bookings": my_bookings})

@login_required(login_url='/login/')
def booking_detail(request, booking_id):
    the_booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, "booking_detail.html",{"booking": the_booking})

@login_required(login_url='/login/')
def make_a_booking(request, asset_id):
    the_asset = get_object_or_404(Asset, pk=asset_id)
    return render(request, "new_booking.html", {"the_asset": the_asset})

@login_required(login_url='/login/')
def all_bookings(request, asset_id):
    the_asset = get_object_or_404(Asset, pk=asset_id)
    all_bookings = Booking.objects.all().filter(asset_ID=the_asset).filter(start_date__gt=datetime.date.today())
    return render(request, "all_bookings.html", {"asset": the_asset, "all_bookings": all_bookings})
