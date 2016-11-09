from assets.models import Asset, Asset_User_Mapping
from accounts.models import User
from django.conf import settings

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
