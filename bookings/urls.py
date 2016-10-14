from django.conf.urls import url
import views

urlpatterns = [
    url(r'^bookings/$', views.bookings, name ="bookings"),
    url(r'^booking/(?P<booking_id>\d+)/$', views.booking_detail, name="booking_detail"),
    url(r'^booking/new/asset/(?P<asset_id>\d+)/$', views.make_a_booking, name="make_a_booking"),
    url(r'^bookings/all/asset/(?P<asset_id>\d+)/$', views.all_bookings, name ="all_bookings"),
]