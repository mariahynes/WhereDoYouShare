from django.conf.urls import url
import views

urlpatterns = [
    url(r'^bookings/$', views.my_bookings, name ="my_bookings"),
    url(r'^booking/(?P<booking_id>\d+)/$', views.booking_detail, name="booking_detail"),
    url(r'^booking/new/asset/(?P<asset_id>\d+)/$', views.make_a_booking, name="make_a_booking"),
    url(r'^bookings/all/asset/(?P<asset_id>\d+)/$', views.all_future_asset_bookings, name ="all_future_asset_bookings"),
    url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<user_id>\d+)/$', views.all_future_asset_bookings, name ="all_future_asset_bookings_for_user"),

]