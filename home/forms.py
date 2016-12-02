from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings

class ContactForm(forms.Form):

# code taken from http://djangobook.com/tying-forms-views/

    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False, label="You email address")
    message = forms.CharField(widget=forms.Textarea, label="Your Message")

    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("You haven't said much. Please expand!")
        return message






