from django.contrib import admin
from .models import Asset,Asset_User_Mapping,AssetType,DurationType

# Register your models here.
admin.site.register(Asset)
admin.site.register(Asset_User_Mapping)
admin.site.register(AssetType)
admin.site.register(DurationType)
