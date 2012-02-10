from django import forms 
from calendar_event.models import CalendarEvent, Reservation

class ReservationCancellationForm(forms.Form):
    
    id_hash = forms.CharField(widget=forms.HiddenInput)
    cancel_reservation_field = forms.BooleanField(label='Cancel Reservation?')#, required=True)

    def init(self, id_hash):   
        self.fields['id_hash'].initial = id_hash
   
    def cancel_reservation(self):
        id_hash = self.cleaned_data.get('id_hash', None)

        if id_hash is None:
            return None
            
        try:
            res = Reservation.objects.get(id_hash=id_hash)
        except Reservation.DoesNotExist:
            return None
            
        res.is_cancelled = True
        res.save()
        
        return res
        