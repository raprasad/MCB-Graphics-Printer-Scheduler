from django import forms
from reservation_type.models import ReservationType

class ReservationTypeForm(forms.ModelForm):
    """Make sure end time is after start time"""

    
    def clean(self):
        """Make sure that the opening and closing times are valid"""
        
        opening_time = self.cleaned_data.get('opening_time', None)
        closing_time = self.cleaned_data.get('closing_time', None)

        if opening_time is None:
            self._errors['opening_time'] = self.error_class(['This field is required.'])
            raise forms.ValidationError('Please enter an opening time')

        if closing_time is None:
            self._errors['closing_time'] = self.error_class(['This field is required.'])
            raise forms.ValidationError('Please enter a closing time')

        if closing_time <= opening_time:
            self._errors['closing_time'] = self.error_class(['The closing time must be after the opening time.'])
            raise forms.ValidationError('Please enter a valid closing time.')
        
        """Make sure that the start and end dates are valid"""
        """
        start/end dates must both be filled in, or both be None
        start/end dates cannot overlap with other ReservationType dates
        """
        start_date = self.cleaned_data.get('start_date', None)
        end_date = self.cleaned_data.get('end_date', None)
        if start_date is None and end_date is None:
            # all set, this is ok
            return self.cleaned_data 
        
        # Only one of start_date/end_date is filled in 
        if start_date is None and end_date is not None:
            self._errors['start_date'] = self.error_class(['If you have an end date, you must have a start date.'])
            raise forms.ValidationError('Please enter a start date')

        if end_date is None and start_date is not None:
            self._errors['end_date'] = self.error_class(['If you have a start date, you must have an end date.'])
            raise forms.ValidationError('Please enter an end date')
        
        if start_date > end_date:
            self._errors['end_date'] = self.error_class(['The end date cannot be before the start date.'])
            raise forms.ValidationError('Please enter an end date')
            

        """
            - check if previous session ended during the new session
            - check if a previous session started during the new session 
            - check if a previous session "encompassed" the new session
        """
        id_to_exclude = None
        if self.instance and self.instance.id:
            id_to_exclude = self.instance.id
        
        # conflict check        
        err_date_overlap_msg = 'Please enter different start/end dates.  (No overlaps are allowed, even if other ReservationTypes are inactive.)'
        if ReservationType.objects.exclude(id=id_to_exclude).filter(end_date__gte=start_date, end_date__lte=end_date).count() > 0:
            self._errors['end_date'] = self.error_class(['Another ReservationType ends during these dates.'])
            self._errors['start_date'] = self.error_class(['Another ReservationType ends during these dates.'])
            raise forms.ValidationError(err_date_overlap_msg)

        if ReservationType.objects.exclude(id=id_to_exclude).filter(start_date__gte=start_date, start_date__lte=end_date).count() > 0:
            self._errors['start_date'] = self.error_class(['Another ReservationType starts during these dates.'])
            self._errors['end_date'] = self.error_class(['Another ReservationType starts during these dates.'])
            raise forms.ValidationError(err_date_overlap_msg)

        if ReservationType.objects.exclude(id=id_to_exclude).filter(start_date__lte=start_date, end_date__gte=end_date).exclude(id=id_to_exclude).count() > 0:
            self._errors['start_date'] = self.error_class(['The start date overlaps with another ReservationType.'])
            self._errors['end_date'] = self.error_class(['The end date overlaps with another ReservationType.'])
            raise forms.ValidationError(err_date_overlap_msg)
            
            
    
        return self.cleaned_data
