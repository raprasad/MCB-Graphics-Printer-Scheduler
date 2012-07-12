from django import forms

class DesignImageAdminForm(forms.ModelForm):
    '''ImageRecord Form.'''

    class Meta:
        widgets = {   'name': forms.TextInput(attrs={'size':20})\
                    , 'description': forms.Textarea(attrs={'rows': 2, 'cols':20})                
                }

