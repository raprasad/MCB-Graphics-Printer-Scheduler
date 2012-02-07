from django import forms

class TimeCheckForm(forms.ModelForm):
    """Make sure end time is after start time"""
    
    def clean(self):
        """Make sure that the chosen instructor is one of those specified for the given semester"""
        start_datetime = self.cleaned_data.get('start_datetime', None)
        end_datetime = self.cleaned_data.get('end_datetime', None)

        if start_datetime is None:
            self._errors['start_datetime'] = self.error_class(['This field is required.'])
            raise forms.ValidationError('Please enter a start time')

        if end_datetime is None:
            self._errors['end_datetime'] = self.error_class(['This field is required.'])
            raise forms.ValidationError('Please enter an end time')

        if end_datetime <= start_datetime:
            self._errors['end_datetime'] = self.error_class(['The end time must be after the start time.'])
            raise forms.ValidationError('Please enter a valid end time.')
        
        return self.cleaned_data
