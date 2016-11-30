from assets.models import Asset, Asset_User_Mapping
from blog.models import Post as BlogPost
from forum.models import Post as ForumPost
from forum.models import Subject, Thread
from accounts.models import User
import json

def can_user_register(user_email):

    try:
        the_user = User.objects.get(username=user_email)
    except User.DoesNotExist:
        can_register = True

    else:
        can_register = False

    return can_register

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

def check_user_linked_to_owner(user_id, owner_id, asset_id):

    # this function checks to see if the user_id has been invited by the owner_id
    # to be a member sharing the asset_id
    # if they have then this function returns TRUE
    try:
        user_linking = Asset_User_Mapping.objects.get(user_ID_id=user_id, inviter_id=owner_id, asset_ID_id=asset_id)

    except Asset_User_Mapping.DoesNotExist:
        user_is_linked_to_owner = False

    else:
        user_is_linked_to_owner = True

    return user_is_linked_to_owner

def check_if_user_is_an_owner(user_id, asset_id):

    # this function checks to see if the user_id is the owner_id
    # for the given asset_id
    # if they are then this function returns TRUE
    try:
        user_linking = Asset_User_Mapping.objects.get(user_ID_id=user_id, is_owner=True, asset_ID_id=asset_id)

    except Asset_User_Mapping.DoesNotExist:
        user_is_an_owner = False

    else:
        user_is_an_owner = True

    return user_is_an_owner

def check_user_linked_to_blog_post(user_id, asset_id, post_id):

    # this function can be used to check if the user is the author of a blog post
    # to check if the user is just chancing their arm trying to edit a blog post

    try:
        user_mapping = BlogPost.objects.get(author_id=user_id, asset_ID_id=asset_id, id=post_id)

    except BlogPost.DoesNotExist:
        user_is_authorised = False

    else:
        user_is_authorised = True

    return user_is_authorised

def check_user_linked_to_forum_post(user_id, post_id):

    # this function can be used to check if the user is the author of a forum/thread post
    # to check if the user is just chancing their arm trying to edit a forum/thread post

    try:
        user_mapping = ForumPost.objects.get(user_id=user_id, id=post_id)

    except ForumPost.DoesNotExist:
        user_is_authorised = False

    else:
        user_is_authorised = True

    return user_is_authorised


def blog_post_exists(asset_id, post_id):

    # check if the post exists for the given asset

    try:
        the_post = BlogPost.objects.get(id=post_id, asset_ID_id=asset_id)

    except BlogPost.DoesNotExist:
        post_exists = False

    else:
        post_exists = True

    return post_exists

def check_thread_exists(subject_id, thread_id):

    # check if the thread exists for the given subject
    try:
        the_thread = Thread.objects.get(id=thread_id, subject_id = subject_id)

    except Thread.DoesNotExist:
        thread_exists = False

    else:
        thread_exists = True

    return thread_exists

def check_subject_exists(asset_id, subject_id):

    # check if the subject exists for the given asset
    try:
        the_subject = Subject.objects.get(id=subject_id, asset_id = asset_id)

    except Subject.DoesNotExist:
        subject_exists = False

    else:
        subject_exists = True

    return subject_exists

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



