from django import forms
from bookings.models import Booking, BookingDetail
import datetime

# created this custom widget because date form fields were
# defaulting to 'text'
# found the solution here: http://stackoverflow.com/questions/22846048/django-form-as-p-datefield-not-showing-input-type-as-date
class DateInput(forms.DateInput):
    input_type = "date"
    # format="%d-%m-%Y"

class BookingForm(forms.ModelForm):

    # start_date = forms.DateField(label="Start Date", widget=DateInput, input_formats=['%d-%m-%Y'])
    # end_date = forms.DateField(label="End Date", widget=DateInput,input_formats=['%d-%m-%Y'])
    start_date = forms.DateField(label="I need it from", widget=DateInput )
    end_date = forms.DateField(label="I will give it back on", widget=DateInput)

    def clean_start_date(self):

        #start date must be in the future
        user_start = self.cleaned_data['start_date']
        if user_start < datetime.date.today():
            raise forms.ValidationError("Please enter a future date")

        return user_start

    def clean_end_date(self):

        # end date must be in the future
        user_end = self.cleaned_data['end_date']
        if user_end <= datetime.date.today():
            raise forms.ValidationError("Please enter a future date")

        return user_end

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']



class BookingDetailForm_for_Owner(forms.ModelForm):


    booking_date = forms.DateField(widget=forms.widgets.DateInput(format="%d-%m-%Y"))

    class Meta:
        model = BookingDetail
        fields = ['id','booking_date','is_approved', 'is_denied']