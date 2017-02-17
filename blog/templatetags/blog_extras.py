import arrow
from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
def started_time(created_date):

   return arrow.get(created_date).humanize()