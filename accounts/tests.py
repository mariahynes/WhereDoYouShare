from django.test import TestCase
from .models import User
from .forms import UserRegistrationForm
from django import forms
from django.conf import settings

class CustomUserTest(TestCase):

    def test_manager_create(self):
        user = User.objects._create_user(None, "test@test.com",
                                         "password",
                                         False, False)
        self.assertIsNotNone(user)

        with self.assertRaises(ValueError):
            user = User.objects._create_user(None, None, "password",
                                             False, False)

    # test form with correct values
    def test_registration_form(self):
        form = UserRegistrationForm({
            'email': "test@test.com",
            'password1': "testpassword",
            'password2': "testpassword",
            'first_name': "me",
            'last_name': "too"

        })

        self.assertTrue(form.is_valid())

    # test form with missing fields, e.g leave out the email
    def test_registration_form_missing_email(self):
        form = UserRegistrationForm({
            'password1': "testpassword",
            'password2': "testpassword",
            'first_name': "me",
            'last_name': "too"

        })

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError,"Please enter your email address!", form.full_clean())

    # test form with missing fields, e.g leave out the password1
    def test_registration_form_missing_password1(self):
        form = UserRegistrationForm({
            'email': "test@test.com",
            'password2': "testpassword",
            'first_name': "me",
            'last_name': "too"

        })

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError, "Please enter a password!", form.full_clean())

    # test form with missing fields, e.g leave out the second password
    def test_registration_form_missing_password2(self):
        form = UserRegistrationForm({
            'email': "test@test.com",
            'password1': "testpassword",
            'first_name': "me",
            'last_name': "too"

        })

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError, "Please re-enter the password!", form.full_clean())

    # test form with missing fields, e.g leave out the first name
    def test_registration_form_missing_first_name(self):
        form = UserRegistrationForm({
            'email': "test@test.com",
            'password1': "testpassword",
            'password2': "testpassword",
            'last_name': "too"

        })

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError, "Please enter your first name!", form.full_clean())

    # test form with missing fields, e.g leave out the last name
    def test_registration_form_missing_last_name(self):
        form = UserRegistrationForm({
            'email': "test@test.com",
            'password1': "testpassword",
            'password2': "testpassword",
            'first_name': "me"

        })

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError, "Please enter your surname!", form.full_clean())

    # test form with passwords that don't match
    def test_registration_form_unmatch_passwords(self):
        form = UserRegistrationForm({
            'email': "test@test.com",
            'password1': "testword",
            'password2': "testpassword",
            'first_name': "me",
            'last_name': "too"

        })

        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(forms.ValidationError, "Those passwords do not match!", form.full_clean())