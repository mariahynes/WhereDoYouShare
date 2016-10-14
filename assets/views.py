from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from assets.models import Asset

@login_required(login_url='/login/')
def assets(request):
    my_id = request.user
    my_assets = Asset.objects.filter(asset_users=my_id)
    return render(request,"assets.html", {"assets": my_assets})

@login_required(login_url='/login/')
def asset_detail(request, asset_id):
    the_asset = get_object_or_404(Asset, pk=asset_id)
    return render(request, "asset_detail.html",{"asset": the_asset})