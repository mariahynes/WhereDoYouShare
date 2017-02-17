from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from assets.models import Asset
from home.myAuth import check_user_linked_to_asset
from django.core.urlresolvers import reverse

@login_required(login_url='/login/')
def assets(request):
    my_id = request.user
    my_assets = Asset.objects.all().filter(asset_users=my_id)
    return render(request,"assets.html", {"assets": my_assets})

@login_required(login_url='/login/')
def asset_detail(request, asset_id):

    the_asset = get_object_or_404(Asset, pk=asset_id)

    errors = []

    # check if the user is allowed to view this asset
    my_id = request.user

    if check_user_linked_to_asset(my_id, asset_id) == False:
        the_asset = []
        errors.append("You are not authorised to view this page")

    return render(request, "asset_detail.html",{"asset": the_asset, "errors": errors})

