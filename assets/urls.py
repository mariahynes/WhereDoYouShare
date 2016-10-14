from django.conf.urls import url
import views

urlpatterns = [
    url(r'^assets/$', views.assets, name ="assets"),
    url(r'^asset/(?P<asset_id>\d+)/$', views.asset_detail, name="asset_detail"),
]