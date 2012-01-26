from django import forms

class ReservationTypeForm(forms.ModelForm):
    """Make sure end time is after start time"""
    
    def clean(self):
        """Make sure that the chosen instructor is one of those specified for the given semester"""
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
        
        return self.cleaned_data
