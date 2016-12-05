from django.test import TestCase
from bookings.views import my_bookings, booking_detail, delete_booking, make_a_booking,all_asset_bookings
from assets.models import Asset, Asset_User_Mapping
from django.core.urlresolvers import resolve
from accounts.models import User
from bookings.models import Booking


class BookingPageTest(TestCase):

    fixtures = ['assets', 'user', 'booking', 'asset_user_mapping']

    # url(r'^bookings/$', views.my_bookings, name ="my_bookings"),
    def test_bookings_page_resolves(self):
        bookings_page = resolve('/booking/bookings/')
        self.assertEqual(bookings_page.func, my_bookings)

    # url(r'^booking/(?P<booking_id>\d+)/$', views.booking_detail, name="booking_detail"),
    def test_booking_detail_page_resolves(self):
        booking = Booking.objects.all()[0]
        booking_id = booking.booking_id
        the_url = '/booking/booking/%s/' % booking_id
        bookings_page = resolve(the_url)
        self.assertEqual(bookings_page.func, booking_detail)

    # url(r'^booking/(?P<booking_id>\d+)/delete/$', views.delete_booking, name="delete_booking"),
    def test_booking_delete_page_resolves(self):
        booking = Booking.objects.all()[0]
        booking_id = booking.booking_id
        the_url = '/booking/booking/%s/delete/' % booking_id
        bookings_page = resolve(the_url)
        self.assertEqual(bookings_page.func, delete_booking)

    # url(r'^booking/(?P<booking_id>\d+)/(?P<new>[a-z]{3})/$', views.booking_detail, name="booking_detail"),
    def test_booking_new_page_resolves(self):
        booking = Booking.objects.all()[0]
        booking_id = booking.booking_id
        the_url = '/booking/booking/%s/new/' % booking_id
        bookings_page = resolve(the_url)
        self.assertEqual(bookings_page.func, booking_detail)

    # url(r'^booking/new/asset/(?P<asset_id>\d+)/$', views.make_a_booking, name="make_a_booking"),
    def test_booking_make_new_page_resolves(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        the_url = '/booking/booking/new/asset/%s/' % asset_id
        bookings_page = resolve(the_url)
        self.assertEqual(bookings_page.func, make_a_booking)

    # url(r'^bookings/all/asset/(?P<asset_id>\d+)/$', views.all_asset_bookings, name ="all_asset_bookings"),
    def test_booking_all_assets_page_resolves(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        the_url = '/booking/bookings/all/asset/%s/' % asset_id
        bookings_page = resolve(the_url)
        self.assertEqual(bookings_page.func, all_asset_bookings)

    # url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<time_period>[a-z]{1,9})/$', views.all_asset_bookings, name ="all_asset_bookings"),
    def test_booking_all_assets_page_future_time_resolves(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        the_url = '/booking/bookings/all/asset/%s/future/' % asset_id
        bookings_page = resolve(the_url)
        self.assertEqual(bookings_page.func, all_asset_bookings)

    # url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<time_period>[a-z]{1,9})/$', views.all_asset_bookings, name ="all_asset_bookings"),
    def test_booking_all_assets_page_past_time_resolves(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        the_url = '/booking/bookings/all/asset/%s/past/' % asset_id
        bookings_page = resolve(the_url)
        self.assertEqual(bookings_page.func, all_asset_bookings)

    # url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<user_id>\d+)/$', views.all_asset_bookings, name ="all_asset_bookings"),
    def test_booking_all_assets_page_user_resolves(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        users = User.objects.all()[0]
        user = users.id
        the_url = '/booking/bookings/all/asset/%s/%s/' % (asset_id, user)
        bookings_page = resolve(the_url)
        self.assertEqual(bookings_page.func, all_asset_bookings)

    # url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<user_id>\d+)/(?P<time_period>[a-z]{1,9})/$', views.all_asset_bookings, name ="all_asset_bookings"),
    def test_booking_all_assets_page_usesr_past_time_resolves(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        users = User.objects.all()[0]
        user = users.id
        the_url = '/booking/bookings/all/asset/%s/%s/past/' % (asset_id, user)
        bookings_page = resolve(the_url)
        self.assertEqual(bookings_page.func, all_asset_bookings)

    # url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<user_id>\d+)/(?P<time_period>[a-z]{1,9})/$', views.all_asset_bookings, name ="all_asset_bookings"),
    def test_booking_all_assets_page_user_future_time_resolves(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        users = User.objects.all()[0]
        user = users.id
        the_url = '/booking/bookings/all/asset/%s/%s/future/' % (asset_id, user)
        bookings_page = resolve(the_url)
        self.assertEqual(bookings_page.func, all_asset_bookings)

    # url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<user_id>\d+)/(?P<time_period>[a-z]{1,9})/(?P<status>[a-z]{1,10})/$', views.all_asset_bookings, name ="all_asset_bookings"),
    def test_booking_all_assets_page_user_future_pending_resolves(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        users = User.objects.all()[0]
        user = users.id
        the_url = '/booking/bookings/all/asset/%s/%s/future/pending/' % (asset_id, user)
        bookings_page = resolve(the_url)
        self.assertEqual(bookings_page.func, all_asset_bookings)

    # url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<user_id>\d+)/(?P<time_period>[a-z]{1,9})/(?P<status>[a-z]{1,10})/$', views.all_asset_bookings, name ="all_asset_bookings"),
    def test_booking_all_assets_page_user_future_confirmed_resolves(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        users = User.objects.all()[0]
        user = users.id
        the_url = '/booking/bookings/all/asset/%s/%s/future/confirmed/' % (asset_id, user)
        bookings_page = resolve(the_url)
        self.assertEqual(bookings_page.func, all_asset_bookings)


    # url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<user_id>\d+)/(?P<time_period>[a-z]{1,9})/(?P<status>[a-z]{1,10})/$', views.all_asset_bookings, name ="all_asset_bookings"),
    def test_booking_all_assets_page_user_future_confirming_resolves(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        users = User.objects.all()[0]
        user = users.id
        the_url = '/booking/bookings/all/asset/%s/%s/future/confirming/' % (asset_id, user)
        bookings_page = resolve(the_url)
        self.assertEqual(bookings_page.func, all_asset_bookings)

    # url(r'^bookings/all/asset/(?P<asset_id>\d+)/(?P<user_id>\d+)/(?P<time_period>[a-z]{1,9})/(?P<status>[a-z]{1,10})/(?P<owner_id>\d+)/$', views.all_asset_bookings, name ="all_asset_bookings"),
    def test_booking_all_assets_page_user_future_pending_with_owner_resolves(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        users = User.objects.all()[0]
        user = users.id
        owners = Asset_User_Mapping.objects.all().filter(asset_ID_id=asset_id, is_owner = True)[0]
        owner = owners.id
        the_url = '/booking/bookings/all/asset/%s/%s/future/confirming/%s/' % (asset_id, user, owner)
        bookings_page = resolve(the_url)
        self.assertEqual(bookings_page.func, all_asset_bookings)