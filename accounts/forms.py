from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User, StripeDetail
from django.core.exceptions import ValidationError


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput
    )

    first_name = forms.CharField(
        label="First Name"
    )

    last_name = forms.CharField(
        label="Surname"
    )

    email = forms.CharField(
        label="Email",
        widget = forms.EmailInput
    )

    class Meta:
        model = User
        fields = ['email', 'first_name','last_name','password1', 'password2']
        exclude = ['username']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            message = "Passwords do not match"
            raise ValidationError(message)

        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            message = "Please enter your email address"
            raise forms.ValidationError(message)

        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if not first_name:
            message = "Please enter your first name"
            raise forms.ValidationError(message)

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if not last_name:
            message = "Please enter your surname"
            raise forms.ValidationError(message)

        return last_name

    def save(self, commit=True):
        instance = super(UserRegistrationForm, self).save(commit=False)

        instance.username = instance.email

        if commit:
            instance.save()

        return instance

class UserLoginForm(forms.Form):
    email = forms.EmailField(label="")
    password = forms.CharField(widget=forms.PasswordInput, label="")


class StripeRegistrationForm(forms.Form):

    #MONTH_CHOICES = [(i,i,) for i in xrange(1,13)]
    MONTH_CHOICES = (
        (1, 'JAN'),
        (2, 'FEB'),
        (3, 'MAR'),
        (4, 'APR'),
        (5, 'MAY'),
        (6, 'JUN'),
        (7, 'JUL'),
        (8, 'AUG'),
        (9, 'SEP'),
        (10, 'OCT'),
        (11, 'NOV'),
        (12, 'DEC'),
    )
    YEAR_CHOICES = [(i,i,) for i in xrange(2016,2036)]

    credit_card_number = forms.CharField(label='Credit Card Number')
    cvv = forms.CharField(max_length=4,label='Security Code (CVV)' )
    expiry_month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES)
    expiry_year = forms.ChoiceField(label='Year', choices=YEAR_CHOICES)
    stripe_id = forms.CharField(widget=forms.HiddenInput) # this field will be saved to the StripeDetails table
                                                          # and this field is hidden because the value in it will be returned
                                                          # from stripe website (i.e. not a user input)

    class Meta:
        model = StripeDetail
        fields = ['stripe_id']

