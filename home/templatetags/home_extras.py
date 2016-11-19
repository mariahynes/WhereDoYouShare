from django import template

register = template.Library()

@register.filter
def get_total_pending(pending_requests,asset_id):

    total = 0

    for booking in pending_requests:
        if asset_id == asset_id:
            total += 1

    return total

