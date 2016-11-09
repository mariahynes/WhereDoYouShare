from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post
from home.myAuth import check_user_linked_to_asset
from assets.models import Asset

def post_list(request, asset_id):

    # this view will return the posts for the given asset_id
    # posts will be ordered by most recent first and
    # only posts with pub date from current date or before

    errors = []

    # check that the asset ID exists
    # if not a 404 will be thrown
    the_asset = get_object_or_404(Asset, pk=asset_id)

    # ok, so asset exists
    # now check that this user is allowed to view posts for this asset
    my_id = request.user

    if check_user_linked_to_asset(my_id, asset_id):
        # user is linked so fill up the posts object
        posts = Post.objects.filter(asset_ID=asset_id, published_date__lte=timezone.now()).order_by('-published_date')

    else:
        # prepare the error message
        errors.append("You are not authorised to view this Blog")
        # set these to empty
        the_asset = []
        posts = []

    return render(request,"blogposts.html", {'posts': posts, 'asset':the_asset, 'errors':errors})




