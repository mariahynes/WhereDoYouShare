from django.contrib import admin
from accounts.models import User, StripeDetail

# Register your models here.
admin.site.register(User)
admin.site.register(StripeDetail)
