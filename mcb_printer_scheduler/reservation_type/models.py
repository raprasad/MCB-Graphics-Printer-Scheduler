from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save

from calendar_user.models import CalendarUser
from schedule_helper.reservation_type_checker import check_reservation_type

from datetime import datetime, timedelta

try:
    from hashlib import sha1
except:
    import md5

"""
DAY_NAMES = "Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split()
DAYS_OF_WEEK = map(lambda x: (x[1], x[0]+1), enumerate(DAY_NAMES))
for x, y in DAYS_OF_WEEK:
    d = DayOfWeek(day=x,day_number=y); d.save()
"""
class DayOfWeek(models.Model):
    day = models.CharField(max_length=10)
    day_number = models.IntegerField()
    
    def __unicode__(self):
        return '%s (%s)' % (self.day, self.day_number)
    
    class Meta:
        ordering = ('day_number',)
        verbose_name = 'Day of Week'
        verbose_name_plural = 'Days of Week'
        
class ReservationType(models.Model):
    """
    Reservation Type - only one may be a default at once

    In addition, date specific reservation types may be active and override the defaults.
    
    Note, date specific reservation types may not overlap
    """
    name = models.CharField(max_length=255)
    
    days_allowed = models.ManyToManyField(DayOfWeek, blank=True, null=True)
    day_iso_numbers = models.CharField('ISO day numbers', max_length=30, blank=True, help_text='auto-filled on save')
    
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    time_block = models.IntegerField('minutes in a time block', default=20)

    is_active = models.BooleanField(default=False)
    is_default = models.BooleanField(default=False)
    
    id_hash = models.CharField(max_length=40, blank=True, help_text='Auto-fill on save')   # 
    
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-is_default', '-is_active',)

    def get_day_iso_numbers(self):
        l = map(lambda x: x.day_number, self.days_allowed.all())
        if len(l) == 0:
            return ''
        else:
            return str(l)   # e.g. [1, 2, 3, 4, 5, 6, 7]
        
    def __unicode__(self):
        return self.name
    
    def available_days_of_week(self):
        l = map(lambda x: x.day, self.days_allowed.all())
        if len(l) == 0:
            return 'none'
        return '<br />'.join(l)
    available_days_of_week.allow_tags = True    
    
        
    def save(self):    
        if self.id == None:
            super(ReservationType, self).save()     
                 
        try:
            self.id_hash =  sha1('%s%s' % (self.id,  self.name)).hexdigest()
        except: #md5 is for old versions of python
            self.id_hash =  md5.new('%s%s' % (self.id,  self.name)).hexdigest()
        
        super(ReservationType, self).save()    

    def is_calendar_event_valid(self, calendar_event):
        """Check if a calendar event meets the requirements of this event type.
        Very rudimentary check.  (Not checking for scheduling conflicts.)"""
        
        if calendar_event is None:
            return False

        if calendar_event.__dict__.get('start_time', None) is None:
            return False

        if calendar_event.__dict__.get('end_time', None) is None:
            return False
            
        # Is this a valid day of the week
        #print self.day_iso_numbers
        if not calendar_event.start_time.isoweekday() in eval(self.day_iso_numbers):
            return False

        # start time is too early or too late
        if calendar_event.start_time.time() < self.opening_time or calendar_event.start_time.time() > self.closing_time:
            return False

        # end time is too early or too late
        if calendar_event.end_time.time() < self.opening_time or calendar_event.end_time.time() > self.closing_time:
            return False

        if not calendar_event.get_event_length_in_minutes() == self.time_block:
            return False

        return True

post_save.connect(check_reservation_type, sender=ReservationType)

    