from django.conf.urls import url
import views

urlpatterns = [
    url(r'^bookings/$', views.my_bookings, name ="my_bookings"),
    url(r'^booking/(?P<booking_id>\d+)/$', views.booking_detail, name="booking_detail"),
    url(r'^booking/(?P<booking_id>\d+)/delete/$', views.delete_booking, name="delete_booking"),
    url(r'^booking/(?P<booking_id>\d+)/(?P<new>[a-z]{3})/$', views.booking_detail, name="booking_detail"),
    url(r'^booking/new/asset/(?P<asset_id>\d+)/$', views.make_a_booking, name="make_a_booking"),

    url(r'^bookings/all/asset/(?P<asset_id>\d+)/$', views.all_asset_bookings, name ="all_asset_bookings"),
    url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<time_period>[a-z]{1,9})/$', views.all_asset_bookings, name ="all_asset_bookings"),
    url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<user_id>\d+)/$', views.all_asset_bookings, name ="all_asset_bookings"),
    url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<user_id>\d+)/(?P<time_period>[a-z]{1,9})/$', views.all_asset_bookings, name ="all_asset_bookings"),
    url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<user_id>\d+)/(?P<time_period>[a-z]{1,9})/(?P<status>[a-z]{1,10})/$', views.all_asset_bookings, name ="all_asset_bookings"),
    url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<user_id>\d+)/(?P<time_period>[a-z]{1,9})/(?P<status>[a-z]{1,10})/(?P<owner_id>\d+)/$', views.all_asset_bookings, name ="all_asset_bookings"),

]


# def all_bookings(request, asset_id=0, status = "", time_period = "", user_id=0):