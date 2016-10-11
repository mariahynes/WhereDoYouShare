from django.shortcuts import render
from assets.models import Asset_User_Mapping

def assets(request):
    my_id = request.user
    my_assets = Asset_User_Mapping.objects.filter(user_ID=my_id)
    return render(request,"assets/assets.html", {"assets": my_assets})
