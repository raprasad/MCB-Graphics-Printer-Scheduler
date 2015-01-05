from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime, timedelta
from calendar_user.models import CalendarUser
from calendar_event.models import Reservation

class Invoice(models.Model):
    reservation = models.ForeignKey(Reservation)
    invoice_no = models.CharField(max_length=40, blank=True)
    filename = models.CharField(max_length=40, blank=True)
    html = models.TextField(max_length=64000, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
        
    def __unicode__(self):
        return self.invoice_no
    
    class Meta:
        ordering = ('-created', 'invoice_no'  )
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
