from django.contrib import messages, auth
from .forms import UserRegistrationForm, UserLoginForm,StripeRegistrationForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from assets.models import Asset, Asset_User_Mapping
from assets.forms import InviteCodeForm
import datetime
from django.utils import timezone
from django.core import serializers
from home.myAuth import check_user_linked_to_asset, can_user_register
from django.conf import settings
from accounts.models import User, StripeDetail
import stripe

stripe.api_key = settings.STRIPE_SECRET

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
            if cd['invitecode'] == "11111":
                # check if the code has been used
                if check_user_linked_to_asset(request.user,1) == False:
                    new_mapping = Asset_User_Mapping(user_ID=request.user,asset_ID_id=1,date_activated=the_date, is_owner=0,is_activated=True,inviter_id=13)
                    new_mapping.save()
                else:
                    code_message = "You have already used that code"

            elif cd['invitecode'] == "22222":
                if check_user_linked_to_asset(request.user,2) == False:
                    new_mapping = Asset_User_Mapping(user_ID=request.user, asset_ID_id=2, date_activated=the_date, is_owner=0, is_activated=True, inviter_id=21)
                    new_mapping.save()
                else:
                    code_message = "You have already used that code"

            elif cd['invitecode'] == "33333":
                if check_user_linked_to_asset(request.user,3) == False:
                    new_mapping = Asset_User_Mapping(user_ID=request.user, asset_ID_id=3, date_activated=the_date, is_owner=0, is_activated=True, inviter_id=19)
                    new_mapping.save()
                else:
                    code_message = "You have already used that code"

            else:
                code_message = "Code not recognised"
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

    assets = Asset_User_Mapping.objects.all().filter(user_ID=request.user)

    return render(request, 'profile.html',
                  {'assets': assets, 'invitecodeform': invitecodeform, 'code_message': code_message})


def login(request):
    errors = []

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
                errors.append("Your details were not recognised")

    else:
        form = UserLoginForm()

    args = {'form': form,
            'errors':errors}

    args.update(csrf(request))
    return render(request, 'login.html', args)

def logout(request):
    auth.logout(request)
    # messages.success(request, 'Come back soon!')
    return redirect(reverse('index'))





def register_stripe(request):

    if request.method == 'POST':
        form = StripeRegistrationForm(request.POST)

        # get this user's email address
        this_user = User.objects.get(pk=request.user.id)
        email_address = this_user.username
        first_name = this_user.first_name
        second_name = this_user.last_name
        first_second_name = "%s %s" % (first_name, second_name)

        print "%s %s" % (this_user, email_address)

        if form.is_valid():
            print "form is valid"
            global customer
            try:

                customer = stripe.Customer.create(
                    source=form.cleaned_data['stripe_id'],
                    description=first_second_name,
                    email=email_address
                )
            except stripe.error.CardError, e:
                messages.error(request, "Your card was declined :-(")

            # check if there is a customer id
            if customer.id:
                print "customer id: %s" % customer.id

                new_stripe = StripeDetail(user_id=request.user,
                                           stripe_id=customer.id)

                new_stripe.save()

                asset_id = request.session.get('asset_id_for_stripe')
                return redirect(reverse('make_a_booking', kwargs={"asset_id": asset_id}))

            else:
                messages.error(request, "Sorry, we are unable to take a payment with that card - no customer id")
        else:
            print "form not valid %s" % form.errors
            messages.error(request, "Sorry, we are unable to take a payment with that card form - no stripe id" )
    else:

        form = StripeRegistrationForm()

    args = {'form': form, 'publishable': settings.STRIPE_PUBLISHABLE}
    args.update(csrf(request))

    return render(request, 'register_stripe.html', args)