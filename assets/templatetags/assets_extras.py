
from django import template
from django.core.urlresolvers import reverse
from django.conf import settings
from assets.models import Asset_User_Mapping
register = template.Library()

@register.filter
def my_asset_count(asset_user_mapping):
    total_assets = asset_user_mapping.objects.count(requested_by_User_ID=settings.AUTH_USER_MODEL)

    return total_assets

@register.simple_tag
def get_total_asset_members(asset_id):

    total_members = 0
    all_users = Asset_User_Mapping.objects.all().filter(asset_ID_id=asset_id, is_owner=False)

    total_members = all_users.count()


    return total_members

@register.simple_tag
def get_total_asset_owners(asset_id):

    total_owners = 0
    all_owners = Asset_User_Mapping.objects.all().filter(asset_ID_id=asset_id, is_owner=True)

    total_owners = all_owners.count()


    return total_owners