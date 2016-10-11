from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from assets.models import Asset, Asset_User_Mapping
from .models import Booking
from accounts.models import User
from django.conf import settings


def booking(request):
    my_id = request.user
    my_bookings = Booking.objects.filter(requested_by_user_ID=my_id)
    return render(request,"booking/bookings.html", {"bookings": my_bookings})