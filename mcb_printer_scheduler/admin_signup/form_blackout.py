import re
from django import forms 
from datetime import timedelta

from reservation_type.conflict_checker import ConflictChecker
from reservation_type.time_slot_maker import TimeSlot

from calendar_event.models import CalendarMessage



class AdminBlackoutForm(forms.Form):
    """Form used for a regular user to reserve a time."""

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
             self._errors['time_slot'] = self.error_class(['Please choose a different time.'])
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
