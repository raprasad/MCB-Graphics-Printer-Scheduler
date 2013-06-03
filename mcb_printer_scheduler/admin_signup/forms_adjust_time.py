import re
from django import forms 
from datetime import datetime, time, timedelta

from reservation_type.models import DayOfWeek, ReservationType, DEFAULT_TIME_BLOCK
from reservation_type.time_slot_maker import TimeSlotChecker

# 15 minute slots
#
#
class AvailableHoursForm(forms.Form):
    
    # Start | End | Last Start Time - assumes DEFAULT_TIME_BLOCK is 15 minutes
    SLOT1_TIMES = ( time(9, 00), time(11, 30), time(11, 30-DEFAULT_TIME_BLOCK))
    SLOT2_TIMES = ( time(11, 30), time(18, 00),  time(17, 60-DEFAULT_TIME_BLOCK))
    SLOT3_TIMES = ( time(18, 00), time(21, 00),  time(20, 60-DEFAULT_TIME_BLOCK))

    """Blackout a Time Slot"""
    selected_day = forms.DateField(widget=forms.HiddenInput)
    slot1 = forms.BooleanField(label='9:00am to 11:30am', required=False)
    slot2 = forms.BooleanField(label='11:30am to 6pm', required=False, help_text='(last reservation starts at 5:45pm)')
    slot3 = forms.BooleanField(label='6pm to 9:00pm', help_text='(last reservation starts at 8:45pm)', required=False)

    def init(self, selected_day):
        self.fields['selected_day'].initial = selected_day
        
    def clean(self):
        """Make sure at least one time slot is fixed"""
        slot1 = self.cleaned_data.get('slot1', False)
        slot2 = self.cleaned_data.get('slot2', False)
        slot3 = self.cleaned_data.get('slot3', False)

        if not (slot1 or slot2 or slot3):
            self._errors['slot1'] = self.error_class(['At least one time period is required.'])
            raise forms.ValidationError('Please choose at least one time period.')
        
        if slot1 and slot3 and not slot2:
            self._errors['slot2'] = self.error_class(['The times picked must be continuous.'])
            raise forms.ValidationError('Please choose adjacent time slots, or a single time slot.')
                
        return self.cleaned_data

    
    def get_earliest_time(self):
        if self.cleaned_data.get('slot1', False):
            return self.SLOT1_TIMES[0]

        if self.cleaned_data.get('slot2', False):
            return self.SLOT2_TIMES[0]

        if self.cleaned_data.get('slot3', False):
            return self.SLOT3_TIMES[0]
        
    
    def get_latest_time(self):
        if self.cleaned_data.get('slot3', False):
            return self.SLOT3_TIMES[2]

        if self.cleaned_data.get('slot2', False):
            return self.SLOT2_TIMES[2]

        if self.cleaned_data.get('slot1', False):
            return self.SLOT1_TIMES[2]


    def make_new_reservation_type(self):
        if not self.is_valid():
            return False
        
        selected_day = self.cleaned_data['selected_day']
    
        print 'get_earliest_time', self.get_earliest_time()
        print 'get_latest_time', self.get_latest_time()
        print 'SLOT1_TIMES', self.SLOT1_TIMES
        print self.cleaned_data
        
        new_rt = ReservationType(name='time for %s' % selected_day.strftime('%Y-%m-%d')\
                            , start_date=selected_day\
                            , end_date=selected_day\
                            , time_block=DEFAULT_TIME_BLOCK
                            , opening_time=self.get_earliest_time()\
                            , closing_time=self.get_latest_time()\
                            , is_active=True
                            )
        new_rt.save()
        
        for d in DayOfWeek.objects.all():
            new_rt.days_allowed.add(d)
        new_rt.save()
        new_rt.save()
        
        ## Turn off other Reservation Types for this day
        l = TimeSlotChecker.get_potential_reservation_types(selected_day)
        for rt in l:
            if not (rt.is_default or new_rt.id==rt.id):
                rt.is_active=False
                rt.save()
        
        return True
        
        
        
        
        
        
        
        