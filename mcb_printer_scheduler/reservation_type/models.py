from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save

from calendar_user.models import CalendarUser
from schedule_maker.reservation_type_checker import check_reservation_type

from datetime import datetime, timedelta

try:
    from hashlib import sha1
except:
    import md5
    
#DAY_NAMES = "Sunday Monday Tuesday Wednesday Thursday Friday Saturday".split()
#DAYS_OF_WEEK = map(lambda x: (x[1], x[0]+1), enumerate(DAY_NAMES))
#for x, y in DAYS_OF_WEEK:
#    d = DayOfWeek(day=x,day_number=y); d.save()

class DayOfWeek(models.Model):
    day = models.CharField(max_length=10)
    day_number = models.IntegerField()
    
    def __unicode__(self):
        return '%s (%s)' % (self.day, self.day_number)
    
    class Meta:
        ordering = ('day_number',)
    
        
class ReservationType(models.Model):
    """
    Reservation Type - only one may be active at once
    """
    name = models.CharField(max_length=255)
    
    days_allowed = models.ManyToManyField(DayOfWeek, blank=True, null=True)
    
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    time_block = models.IntegerField('minutes in a time block', default=20)
    is_active = models.BooleanField(default=False)
    
    id_hash = models.CharField(max_length=40, blank=True, help_text='Auto-fill on save')   # 
    
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    
    def __unicode__(self):
        return self.name
    
    def available_days_of_week(self):
        l = map(lambda x: x.day, self.days_allowed.all())
        if len(l) == 0:
            return 'none'
        return '<br />'.l
    available_days_of_week.allow_tags = True    
        
    def save(self):    
        if self.id == None:
            super(ReservationType, self).save()     
                 
        try:
            self.id_hash =  sha1('%s%s' % (self.id,  self.name)).hexdigest()
        except: #md5 is for old versions of python
            self.id_hash =  md5.new('%s%s' % (self.id,  self.name)).hexdigest()
                
        super(ReservationType, self).save()    

post_save.connect(check_reservation_type, sender=ReservationType)

    