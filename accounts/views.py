from django.contrib import messages, auth
from .forms import UserRegistrationForm, UserLoginForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from assets.models import Asset, Asset_User_Mapping
from bookings.models import Booking, BookingDetail
from bookings.templatetags.booking_extras import get_booking_start_date
from assets.forms import InviteCodeForm
import datetime
from django.utils import timezone
from django.core import serializers
from home.myAuth import check_user_linked_to_asset, can_user_register

def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():

            # check if the user has already registered
            if can_user_register(request.POST.get('email')) == False:
                messages.error(request, "Sorry, this email is already registered")

            else:
                form.save()
                user = auth.authenticate(email=request.POST.get('email'),
                                         password=request.POST.get('password1'))

                if user:
                    # messages.success(request, "You have successfully registered")
                    auth.login(request, user)
                    return redirect(reverse('profile'))

                else:
                    messages.error(request, "unable to log you in at this time!")

    else:
        form = UserRegistrationForm()

    args = {'form': form}
    args.update(csrf(request))

    return render(request, 'register.html', args)

@login_required(login_url='/login/')
def profile(request):

    invitecodeform = InviteCodeForm()
    code_message = ""

    if request.method == "POST":
        form = InviteCodeForm(request.POST)
        if form.is_valid():
            # hard-coding the actions here for purposes of testing the concept of using an invitation code
            cd = form.cleaned_data
            the_date = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            if cd['invitecode'] == "12345":
                # check if the code has been used
                if check_user_linked_to_asset(request.user,1) == False:
                    new_mapping = Asset_User_Mapping(user_ID=request.user,asset_ID_id=1,date_activated=the_date, is_owner=0,is_activated=True,inviter_id=13)
                    new_mapping.save()
                else:
                    code_message = "You have already used that code"

            elif cd['invitecode'] == "54321":
                if check_user_linked_to_asset(request.user,2) == False:
                    new_mapping = Asset_User_Mapping(user_ID=request.user, asset_ID_id=2, date_activated=the_date, is_owner=0, is_activated=True, inviter_id=13)
                    new_mapping.save()
                else:
                    code_message = "You have already used that code"

    else:

        invitecodeform = InviteCodeForm()


    # set session values to be used until user logs out
    # store the asset ids they are linked to

    # create empty session list
    request.session['linked_assets']=[]
    linked_asset_count = Asset.objects.all().filter(asset_users=request.user).count()

    # want to store a list in the session
    # http://stackoverflow.com/questions/6720121/serializing-result-of-a-queryset-with-json-raises-error
    class LinkedAssets(object):
        def __init__(self,asset_id):
            self.asset_id = asset_id

        def serialize(self):
            return self.__dict__

    if linked_asset_count > 0:
        # fill the linked_assets session list
        linked_assets = serializers.serialize('json',Asset.objects.all().filter(asset_users = request.user), fields=('id,'))
        request.session['linked_assets'] = linked_assets

    future_bookings = BookingDetail.objects.all().filter(booking_id__requested_by_user_ID=request.user, booking_date__gt=datetime.date.today()).order_by("booking_date")

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
        the_date = datetime.datetime.strptime(the_date,"%d %b %Y")
        the_date = the_date.strftime("%Y%m%d")
        date_and_booking_id.append((the_date,booking_id))

    # and sort by the date before sending to the template
    date_and_booking_id = sorted(date_and_booking_id, key=lambda tup: tup[0])


    assets = Asset_User_Mapping.objects.all().filter(user_ID=request.user)
    pending_requests = BookingDetail.objects.all().filter(slot_owner_id_id=request.user, booking_date__gt=datetime.date.today(),is_confirmed=0)

    return render(request, 'profile.html', {'assets': assets, 'bookings': date_and_booking_id, 'num_bookings':num_bookings, 'pending_requests':pending_requests, 'invitecodeform':invitecodeform, 'code_message': code_message})


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(email=request.POST.get('email'),
                                     password=request.POST.get('password'))

            if user is not None:
                auth.login(request, user)
                # messages.error(request, "You're very welcome in!")
                return redirect(reverse('profile'))
            else:
                form.add_error(None, "Now, this could be our problem, but your either your email or your password was not recognised")

    else:
        form = UserLoginForm()

    args = {'form': form}
    args.update(csrf(request))
    return render(request, 'login.html', args)

def logout(request):
    auth.logout(request)
    # messages.success(request, 'Come back soon!')
    return redirect(reverse('index'))