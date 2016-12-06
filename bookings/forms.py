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
    # start_date = forms.DateField(label="I need it from", widget=DateInput )
    # end_date = forms.DateField(label="I will give it back on", widget=DateInput)
    start_date = forms.CharField(label="I need it from")
    end_date = forms.CharField(label="I will give it back on")
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

    booking_date = forms.CharField(widget=forms.HiddenInput(), required=False)

    # although I won't be using all of the below fields as input fields on the form, I need to have
    # booking_date included so that I can display it
    # I need to have date_approved and date_denied so that I can update them in the view just before saving
    # and I will include is_pending so that when the data gets saved, this will automatically revert back to
    # false (because this is the default setting in the BookingDetail table for this field) and this is handy
    # because the purpose of this form is to ONLY save it if the owner is approving/denying dates
    # once this happens, then NONE OF THIS OWNERS DATES IN THIS BOOKING should be pending

    class Meta:
        model = BookingDetail
        fields = ['booking_date','is_approved', 'is_denied', 'is_pending', 'date_approved','date_denied']

class BookingDetailForm_for_Requestor_to_Confirm(forms.ModelForm):

    booking_date = forms.CharField(widget=forms.HiddenInput(), required=False)

    # although I won't be using all of these below fields as input fields on the form, I need to have
    # booking_date included so that I can display it
    # I need to have date_confirmed so that I can update this in the view just before saving
    # and I will include is_denied so that when the data gets saved, it will automatically change back to
    # false (because this is their default field settings in the BookingDetail table) and this is handy
    # because the purpose of this form is to ONLY save it if the requestor is confirming dates and
    # once this happens, then NONE OF THE REQUESTOR DATES IN THIS BOOKING should be anything other than is_confirmed = True

    is_approved = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = BookingDetail
        fields = ['booking_date','is_approved', 'is_denied', 'is_confirmed', 'date_confirmed']

class BookingDetailForm_for_Requestor_Confirmed_or_Pending(forms.ModelForm):

    booking_date = forms.CharField(widget=forms.HiddenInput(), required=False)

    # I need to have booking_date included so that I can display it
    # other than that, the user will only be allowed to delete

    class Meta:
        model = BookingDetail
        fields = ['booking_date']