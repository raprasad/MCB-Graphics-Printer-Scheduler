import re
from django import forms 
from datetime import timedelta

from reservation_type.conflict_checker import ConflictChecker
from reservation_type.time_slot_maker import TimeSlot

from poster_tube.models import PosterTubeColor, PosterTubeType

from calendar_event.models import CalendarEvent, Reservation

from django.contrib.localflavor.us.forms import USPhoneNumberField

def get_color_choices():
    return map(lambda x: (x.name, x.name), PosterTubeColor.objects.all())

class SignupForm(forms.Form):
    """Form used for a regular user to reserve a time."""

    time_slot = forms.DateTimeField(label='Available times', widget=forms.Select)
    session_length = forms.IntegerField(widget=forms.HiddenInput)
    phone_number = USPhoneNumberField(label='Contact Phone',widget=forms.TextInput(attrs={'size': 25}) )
    email = forms.EmailField(label='Contact Email', widget=forms.TextInput(attrs={'size': 25}) )
    billing_code = forms.CharField(label='33-digit Harvard Billing Code', required=False, widget=forms.TextInput(attrs={'size': 40}))
    lab_name = forms.CharField(label='Lab or Group Affiliation',widget=forms.TextInput(attrs={'size': 25}) )
    poster_tube_type = forms.ModelChoiceField(label='Poster tube (optional)', queryset=PosterTubeType.objects.filter(available=True), required=False)
    poster_tube_color = forms.ChoiceField(choices=get_color_choices(), required=False)
    
    def init(self, time_slot_choices, session_length, cal_user):   
        self.fields['time_slot'].widget.choices = time_slot_choices
        self.fields['session_length'].initial = session_length

        self.fields['email'].initial = cal_user.contact_email 
        self.fields['phone_number'].initial = cal_user.phone_number
        self.fields['billing_code'].initial = cal_user.billing_code
        self.fields['lab_name'].initial = cal_user.lab_name


    def get_time_slot_object(self):
        
        time_slot = self.cleaned_data.get('time_slot', None)
        session_length = self.cleaned_data.get('session_length', None)
        
        try:
            end_datetime = time_slot + timedelta(minutes=session_length)
            return TimeSlot(time_slot, end_datetime)
        except:
            return None
    
    def clean_billing_code(self):
        billing_code = self.cleaned_data.get('billing_code')
        
        if billing_code is None:
            return billing_code

        # remove everything except digits, x's, and dashes
        val = re.sub('[^\d|x|-]', '', billing_code).strip().lower()

        # blanks are OK
        if val == '':
            return val
            
        if not re.match('\d{3}-\d{5}-[x|\d]{4}-\d{6}-\d{6}-\d{4}-\d{5}' ,val):
            raise forms.ValidationError('The code is not 33-digits.  Please re-enter it.')
        
        return val
        
    def clean(self):
        """Make sure the slot is still available"""
        time_slot = self.cleaned_data.get('time_slot', None)
        session_length = self.cleaned_data.get('session_length', None)

        if time_slot is None:
            self._errors['time_slot'] = self.error_class(['This field is required.'])
            raise forms.ValidationError('Please choose an available time')

        if session_length is None:
            self._errors['session_length'] = self.error_class(['This field is required.'])
            raise forms.ValidationError('Please enter a start time')

        ts_obj = self.get_time_slot_object()
        if ts_obj is None:
            raise forms.ValidationError('The time slot is invalid.  Please try again.')
        
        conflict_checker = ConflictChecker()
        if conflict_checker.does_timeslot_conflict(ts_obj):
             self._errors['time_slot'] = self.error_class(['Please choose a different time.'])
             raise forms.ValidationError('Sorry!  Someone reserved that time slot!  Please choose another one.')
        
        """If poster tube chosen, make sure color is chosen"""
        poster_tube_type = self.cleaned_data.get('poster_tube_type')
        poster_tube_color = self.cleaned_data.get('poster_tube_color')
        if poster_tube_type:
            if not poster_tube_color:
                self._errors['poster_tube_color'] = self.error_class(['Please choose a color.'])
                raise forms.ValidationError('If you choose a poster tube, please choose a color.')
        #poster_tube_color = self.cleaned_data.get('poster_tube_color')
        
         
        
        return self.cleaned_data
            
    def get_reservation(self, calendar_user):
        #print '>>> get_reservation'
        if calendar_user is None:
            return None
        
        ts_obj = self.get_time_slot_object()
        if ts_obj is None:
            return None
        
        poster_tube_type = self.cleaned_data.get('poster_tube_type')
        poster_tube_color = self.cleaned_data.get('poster_tube_color')
        if poster_tube_type:
            include_poster_tube = True
            poster_tube_details = '%s; color: %s' % (poster_tube_type, poster_tube_color)
        else:
            include_poster_tube = False
            poster_tube_details = ''
        
        res = Reservation(user=calendar_user\
                        , contact_email=self.cleaned_data.get('email')\
                        , contact_phone=self.cleaned_data.get('phone_number')\
                        , start_datetime = ts_obj.start_datetime\
                        , end_datetime = ts_obj.end_datetime\
                        , billing_code=self.cleaned_data.get('billing_code', '')\
                        , lab_name=self.cleaned_data.get('lab_name', '')\
                        , include_poster_tube=include_poster_tube\
                        , poster_tube_details=poster_tube_details                        
                        )        
        res.save()          # save the reservation
        
        # update user's contact info
        calendar_user.contact_email = res.contact_email
        calendar_user.phone_number = res.contact_phone
        calendar_user.billing_code = res.billing_code
        calendar_user.lab_name = res.lab_name
        calendar_user.save()

        return res
          