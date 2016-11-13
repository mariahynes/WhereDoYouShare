from django.contrib import messages, auth
from .forms import UserRegistrationForm, UserLoginForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from assets.models import Asset
from bookings.models import Booking
import datetime
from django.core import serializers

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
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
        # fill the linked_assets list
       # linked_assets = []

        linked_assets = serializers.serialize('json',Asset.objects.all().filter(asset_users = request.user), fields=('id,'))
      #  linked_assets = serializers.serialize('json', Asset.objects.values('id').filter(asset_users=request.user))
       # linked_assets.append(LinkedAssets(Asset.objects.values_list('id', flat=True)).serialize())
        request.session['linked_assets'] = linked_assets


    # request.session['linked_assets']= Asset.objects.values('id').filter(asset_users=request.user)

    return render(request, 'profile.html', {'assets': Asset.objects.all().filter(asset_users=request.user),
                                            'bookings': Booking.objects.all().filter(requested_by_user_ID=request.user).filter(start_date__gt=datetime.date.today())
                                            })


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
    messages.success(request, 'Come back soon!')
    return redirect(reverse('index'))