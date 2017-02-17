from django.test import TestCase,RequestFactory
from home.views import get_index
from accounts.views import profile, login, register, register_stripe
from django.core.urlresolvers import resolve
from django.shortcuts import render, render_to_response, reverse
from accounts.models import User
from assets.forms import InviteCodeForm

class HomePageTest(TestCase):

    def test_home_page_resolves(self):
        home_page = resolve('/')
        self.assertEqual(home_page.func, get_index)

    def test_home_page_status_code_is_ok(self):
        home_page = self.client.get('/')
        self.assertEquals(home_page.status_code, 200)

    def test_check_content_is_correct(self):
        home_page = self.client.get('/')
        self.assertTemplateUsed(home_page, "index.html")
        home_page_template_output = render_to_response("index.html").content
        self.assertEquals(home_page.content, home_page_template_output)

class LoggedInTests(TestCase):


    def setUp(self):
        super(LoggedInTests, self).setUp()
        self.user = User.objects.create(username='testuser@gmail.com')
        self.user.set_password('123')
        self.user.save()
        self.login = self.client.login(username='testuser@gmail.com',password='123')
        self.assertEqual(self.login,True)


class LoginPageTest(TestCase):

    def test_login_page_resolved(self):
        login_page = resolve('/login/')
        self.assertEqual(login_page.func, login)

    def test_login_page_status_code_is_ok(self):
        login_page = self.client.get('/login/')
        self.assertEquals(login_page.status_code, 200)



class ProfilePageTest(TestCase):
    # url(r'^profile/$',account_views.profile, name='profile'),
    def test_profile_page_resolved(self):
        profile_page = resolve('/profile/')
        self.assertEqual(profile_page.func, profile)


class RegisterPageTest(TestCase):
    # url(r'^profile/$',account_views.profile, name='profile'),
    def test_register_page_resolved(self):
        register_page = resolve('/register/')
        self.assertEqual(register_page.func, register)

    def test_register_page_status_code_is_ok(self):
        register_page = self.client.get('/register/')
        self.assertEquals(register_page.status_code, 200)


class RegisterStripePageTest(TestCase):
    # url(r'^profile/$',account_views.profile, name='profile'),
    def test_registerStripe_page_resolved(self):
        registerStripe_page = resolve('/register_stripe/')
        self.assertEqual(registerStripe_page.func, register_stripe)

    def test_registerStripe_page_status_code_is_ok(self):
        registerStripe_page = self.client.get('/register_stripe/')
        self.assertEquals(registerStripe_page.status_code, 200)
