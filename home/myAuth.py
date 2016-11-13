from assets.models import Asset, Asset_User_Mapping
from blog.models import Post
import json

def check_user_linked_to_asset(user_id, asset_id):

    # this function can be used by any view
    # to check if the user is just chancing their arm trying to view
    # other pages by editing the URL

    try:
        user_mapping = Asset_User_Mapping.objects.get(user_ID_id=user_id, asset_ID_id=asset_id)

    except Asset_User_Mapping.DoesNotExist:
        user_is_authorised = False

    else:
        user_is_authorised = True

    return user_is_authorised

def check_user_linked_to_post(user_id, asset_id, post_id):

    # this function can be used
    # to check if the user is just chancing their arm trying to edit a blog post

    try:
        user_mapping = Post.objects.get(author_id=user_id, asset_ID_id=asset_id, id=post_id)

    except Post.DoesNotExist:
        user_is_authorised = False

    else:
        user_is_authorised = True

    return user_is_authorised

def blog_post_exists(asset_id, post_id):

    try:
        the_post = Post.objects.get(id=post_id, asset_ID_id=asset_id)

    except Post.DoesNotExist:
        post_exists = False

    else:
        post_exists = True

    return post_exists

def check_user_linked_to_asset_with_session(request, asset_id):

    # this is the list of assets saved in the session object (in json format)
    num_linked_assets = request.session['linked_assets']
    # saved into a python object (from json)
    linked_asset_data = json.loads(num_linked_assets)
    #set authoised to false to start with
    user_is_authorised = False

    if len(linked_asset_data)>0:
        for item in linked_asset_data:
            if str(item['pk']) == str(asset_id):
                user_is_authorised = True
                break

    return user_is_authorised



