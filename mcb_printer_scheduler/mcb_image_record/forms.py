from django import forms

class ImageRecordAdminForm(forms.ModelForm):
    '''ImageRecord Form.'''

    class Meta:
        widgets = {  'notes': forms.Textarea(attrs={'rows': 3, 'cols':20}) 
                , 'name': forms.TextInput(attrs={'size':20}) 
                }
