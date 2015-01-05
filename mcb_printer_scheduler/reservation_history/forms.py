from django import forms
from django.forms import widgets, ModelForm
from django.contrib.admin.widgets import AdminDateWidget

from calendar_event.models import CalendarEvent, Reservation
from calendar_user.models import CalendarUser
from media_type.models import PrintMediaType
from poster_tube.models import PosterTubeType
from decimal import Decimal

class CreateInvoiceForm(ModelForm):

    note = forms.CharField(label='Description',
                           required=False,
                           widget=forms.Textarea())
    extra = forms.CharField(label='Extra',
                           required=False,
                           initial='None',
                           widget=forms.Textarea(attrs={'rows': 6}))

    extra_cost = forms.DecimalField(required=False,
                                 label='Extra Cost', 
                                 initial=Decimal('0.00'), 
                                 min_value=Decimal('0.00'),
                                 decimal_places=2,
                                 widget=forms.TextInput(attrs={'size':'8'}))

    sq_feet = forms.DecimalField(required=True,
                                 label='Area in Square feet', 
                                 initial=Decimal('0.0'), 
                                 min_value=Decimal('0.0'),
                                 decimal_places=1,
                                 widget=forms.TextInput(attrs={'size':'8'}))

    billing_date = forms.DateField(label='Invoice Date',
                                  widget=AdminDateWidget())

    completed_date = forms.DateField(label='Date Completed',
                                  widget=AdminDateWidget())

    cc = forms.CharField(max_length=200,
                         required=False)

    PAYMENT_CHOICES = (
        ('ec', 'Harvard Expense Code'),
        ('check', 'Paid with check'),
        ('cash', 'Paid with cash'),
        )

    payment_method = forms.ChoiceField(label='Payment Method',
                                       choices=PAYMENT_CHOICES)


    poster_tube_types = PosterTubeType.objects.all().order_by('name')
    pts = []
    for pt in poster_tube_types:
        pts.append((pt.id, '%s ($%0.2f)' % (pt.name, pt.price)))
    pts.insert(0, pts.pop())

    poster_tube = forms.ChoiceField(label='Poster Tube Types',
                                    choices=pts)
    

    billing_code = forms.CharField(label='Expense Code or Check Number',
                                   required=False,
                                   max_length=39,
                                   widget=forms.TextInput(attrs={'size':'40'}))

    poster_tube_cost = forms.DecimalField(required=False,
                                          initial=Decimal('0.00'), 
                                          min_value=0.0,
                                          decimal_places=2,
                                          widget=forms.HiddenInput(attrs={'readonly': True}))

    has_tax = forms.BooleanField(required=False,
                                 label="Taxable")

    tax = forms.DecimalField(required=False,
                             initial=Decimal('0.00'), 
                             min_value=0.0,
                             decimal_places=2,
                             widget=forms.HiddenInput(attrs={'readonly': True}))

    base_cost = forms.DecimalField(required=False,
                                    initial=Decimal('0.00'), 
                                    min_value=0.0,
                                    decimal_places=2,
                                    widget=forms.HiddenInput(attrs={'readonly': True}))

    subtotal_cost = forms.DecimalField(required=False,
                                    initial=Decimal('0.00'), 
                                    min_value=0.0,
                                    decimal_places=2,
                                    widget=forms.HiddenInput(attrs={'readonly': True}))

    total_cost = forms.DecimalField(required=False,
                                    initial=Decimal('0.00'), 
                                    min_value=0.0,
                                    decimal_places=2,
                                    widget=forms.HiddenInput(attrs={'readonly': True}))

    download_pdf = forms.CharField(required=False, 
                                   initial=False,
                                   widget=forms.HiddenInput())

    class Meta:
        model = Reservation
        widgets = {
          'note': forms.Textarea(attrs={'rows': 3}),
        }
        fields = ('billing_date', 'completed_date', 'note', 'extra', 'extra_cost', 
                  'payment_method', 'billing_code', 'sq_feet', 
                  'print_media', 'poster_tube', 'poster_tube_cost',
                  'tax', 'base_cost', 'subtotal_cost', 'total_cost', 'download_pdf')


