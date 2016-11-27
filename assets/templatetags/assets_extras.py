
from django import template
from django.core.urlresolvers import reverse
from django.conf import settings

register = template.Library()

@register.filter
def my_asset_count(asset_user_mapping):
    total_assets = asset_user_mapping.objects.count(requested_by_User_ID=settings.AUTH_USER_MODEL)

    return total_assets


