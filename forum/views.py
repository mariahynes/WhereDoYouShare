from django.shortcuts import render, redirect, get_object_or_404
from .models import Subject
from home.myAuth import check_user_linked_to_asset
from assets.models import Asset

def forum(request, asset_id):

    errors = []

    # check that the asset ID exists
    # if not a 404 will be thrown
    the_asset = get_object_or_404(Asset, pk=asset_id)

    # ok, so asset exists
    # now check that this user is allowed to view the forum subjects for this asset
    my_id = request.user
    if check_user_linked_to_asset(my_id, asset_id):
        # user is linked so fill up the subjects object
        subjects = Subject.objects.all().filter(asset_id=asset_id)

    else:
        # prepare the error message
        errors.append("You are not authorised to view this Forum")
        # set these to empty
        the_asset = []
        subjects = []

    return render(request, 'forum.html',{'subjects': subjects, 'asset': the_asset, 'errors': errors})


def threads(request, asset_id, subject_id):

    errors = []
    subject = get_object_or_404(Subject, pk=subject_id)
    the_asset = get_object_or_404(Asset, pk=asset_id)

    my_id = request.user
    if check_user_linked_to_asset(my_id, asset_id)==False:
        errors.append("You are not authorised to view this Forum")
        subject = []
        the_asset = []


    return render(request, "threads.html",{'subject': subject, 'asset': the_asset, 'errors': errors})

