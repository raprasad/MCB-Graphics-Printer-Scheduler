import re
from django import forms 
from datetime import datetime, time

from reservation_type.conflict_checker import ConflictChecker
from reservation_type.time_slot_maker import TimeSlot

from calendar_event.models import CalendarMessage, CalendarFullDayMessage



class AdminBlackoutForm(forms.Form):
    """Blackout a Time Slot"""

    message = forms.CharField(label='Message')
    start_time = forms.DateTimeField(label='Start Time', widget=forms.Select)
    end_time = forms.DateTimeField(label='End Time', widget=forms.Select)
    
    def init(self, start_time_choices, end_time_choices):   
        self.fields['start_time'].widget.choices = start_time_choices
        self.fields['end_time'].widget.choices = end_time_choices

        
    def clean(self):
        """Make sure the slot is still available"""
        start_time = self.cleaned_data.get('start_time', None)
        end_time = self.cleaned_data.get('end_time', None)

        if start_time is None:
            self._errors['start_time'] = self.error_class(['This field is required.'])
            raise forms.ValidationError('Please choose a start time')

        if end_time is None:
            self._errors['end_time'] = self.error_class(['This field is required.'])
            raise forms.ValidationError('Please choose an end time')

        if end_time <= start_time:
            self._errors['end_time'] = self.error_class(['This field is required.'])
            raise forms.ValidationError('The end time must be AFTER the start time')
        
        conflict_checker = ConflictChecker()
        if conflict_checker.does_timeslot_conflict(TimeSlot(start_time, end_time)):
             self._errors['end_time'] = self.error_class(['Please choose a different time.'])
             raise forms.ValidationError('Sorry!  That time conflicts with another event reservation or message!  Please choose another one.')
            
        return self.cleaned_data
            
    def get_calendar_event(self):
        start_time = self.cleaned_data.get('start_time', None)
        end_time = self.cleaned_data.get('end_time', None)
    
        if start_time is None or end_time is None:
            return None
                    
        cal_message = CalendarMessage(display_name=self.cleaned_data.get('message')\
                        , start_datetime = start_time\
                        , end_datetime = end_time\
                        )        
        cal_message.save()          # save the CalendarMessage
        
       
        return cal_message






class AdminBlackoutDaysForm(forms.Form):
    """Blackout 1 or More Days"""

    message = forms.CharField(label='Message')
    start_date = forms.DateField(label='Start Date', widget=forms.TextInput)
    end_date = forms.DateField(label='End Date', widget=forms.TextInput)

    def init(self, selected_date):   
        self.fields['start_date'].widget.attrs.update({'readonly':'True'})    
        self.fields['start_date'].initial = selected_date
        self.fields['end_date'].initial = selected_date
        

    def clean(self):
        """Make sure the slot is still available"""
        start_date = self.cleaned_data.get('start_date', None)
        end_date = self.cleaned_data.get('end_date', None)

        if start_date is None:
            self._errors['start_date'] = self.error_class(['This field is required.'])
            raise forms.ValidationError('Please choose a start date')

        if end_date is None:
            self._errors['end_date'] = self.error_class(['This field is required.'])
            raise forms.ValidationError('Please choose an end date')

        if start_date > end_date:
            self._errors['end_date'] = self.error_class(['This field is required.'])
            raise forms.ValidationError('The end date must be AFTER the start date')

        
        start_time = datetime.combine(start_date, time.min)
        end_time = datetime.combine(end_date, time.max)

        conflict_checker = ConflictChecker()
        if conflict_checker.does_timeslot_conflict(TimeSlot(start_time, end_time)):
             self._errors['end_date'] = self.error_class(['Please choose a different date.'])
             raise forms.ValidationError('Sorry!  The start/end dates conflict with another calendar event!  Please choose other dates.')

        return self.cleaned_data


    def get_calendar_event(self):
        start_date = self.cleaned_data.get('start_date', None)
        end_date = self.cleaned_data.get('end_date', None)

        if start_date is None or end_date is None:
            return None

        cal_message = CalendarFullDayMessage(display_name=self.cleaned_data.get('message')\
                        , start_datetime = datetime.combine(start_date, time.min)
                        , end_datetime = datetime.combine(end_date, time.max)
                        )        
        cal_message.save()          # save the CalendarMessage


        return cal_message
