from django import forms
from bookings.models import Booking

# created this custom widget because date form fields were
# defaulting to 'text'
# found the solution here: http://stackoverflow.com/questions/22846048/django-form-as-p-datefield-not-showing-input-type-as-date
class DateInput(forms.DateInput):
    input_type = "date"
    # format="%d-%m-%Y"

class BookingForm(forms.ModelForm):

    # start_date = forms.DateField(label="Start Date", widget=DateInput, input_formats=['%d-%m-%Y'])
    # end_date = forms.DateField(label="End Date", widget=DateInput,input_formats=['%d-%m-%Y'])
    start_date = forms.DateField(label="Start Date", widget=DateInput)
    end_date = forms.DateField(label="End Date", widget=DateInput)

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']



