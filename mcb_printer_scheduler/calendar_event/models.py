from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.localflavor.us.models import PhoneNumberField
from datetime import datetime, timedelta
from calendar_user.models import CalendarUser
try:
    from hashlib import sha1
except:
    import md5
    
class CalendarEvent(models.Model):
    """
    Basic calendar event class
    """
    display_name = models.CharField(max_length=255, blank=True)
    
    id_hash = models.CharField(max_length=40, blank=True, help_text='Auto-fill on save')   # 

    is_visible = models.BooleanField('Event is Active and Visible',     default=True)
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    subclass_type = models.CharField(max_length=70, blank=True, help_text='Event Type (auto-filled on save)')
    
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.display_name
    
    def get_event_length_in_minutes(self):
        if self.end_time is None or self.start_time is None:
            return None
        if self.end_time < self.start_time:
            return None
            
        time_diff = self.end_time - self.start_time
        return time_diff.seconds / 60
        
    def get_display_msg(self):
        if self.display_name:
            return self.display_name
            
        return '%s to %s' % (self.start_time.strftime('%I:%M%p')\
                    , self.end_time.strftime('%I:%M%p')) 
                    
    def save(self):    
        if self.id == None:
            super(CalendarEvent, self).save()     
        
        self.display_name = self.get_display_msg()
         
        try:
            self.id_hash =  sha1('%s%s' % (self.id,  datetime.now())).hexdigest()
        except: #md5 is for old versions of python
            self.id_hash =  md5.new('%s%s' % (self.id,  datetime.now())).hexdigest()
        
        super(CalendarEvent, self).save()    

    class Meta:
        ordering = ('-start_time', 'display_name'  )
        verbose_name = 'Calendar Event (view all events)'
        verbose_name_plural = 'Calendar Events (view all events)'

        
        
class Reservation(CalendarEvent):
    user = models.ForeignKey(CalendarUser)
    contact_email = models.EmailField()
    lab_name = models.CharField(max_length=100)
    billing_code = models.CharField('33 digit billing code', max_length=39, blank=True, help_text='optional, but will expedite paperwork')
    contact_phone = PhoneNumberField(help_text='To contact you regarding scheduling changes.')
    is_cancelled = models.BooleanField(default=False)
    
    def get_display_msg(self):
        return '%s %s-%s' % (self.user.get_first_initial_lastname()\
                            , self.start_time.strftime('%I:%M%p')\
                            , self.end_time.strftime('%I:%M%p')) 
        
    def save(self):    
        if self.is_cancelled:
            self.is_visible= False
        self.subclass_type = self.__class__.__name__
        super(Reservation, self).save()    
    
    
class CalendarMessage(CalendarEvent):
    """For general messages, e.g. holidays, etc"""    
    def get_display_msg(self):
        return self.display_name
    
    def save(self):
        self.subclass_type = self.__class__.__name__
        super(CalendarMessage, self).save()    
        
    class Meta:
        verbose_name = 'Calendar Message'
        verbose_name_plural = 'Calendar Messages'


class CalendarFullDayMessage(CalendarEvent):
    """For general messages, e.g. holidays, etc"""    
    def get_display_msg(self):
        return self.display_name
        
    def save(self):    
        self.start_time = datetime(self.start_time.year, self.start_time.month, self.start_time.day)
        self.end_time = datetime(self.end_time.year, self.end_time.month, self.end_time.day) + timedelta(days=1) + timedelta(microseconds=-1)
        if self.start_time > self.end_time:
            self.end_time = self.start_time + timedelta(days=1) + timedelta(microseconds=-1)
        self.subclass_type = self.__class__.__name__
        
        super(CalendarFullDayMessage, self).save()    

    class Meta:
        verbose_name = 'Calendar Full Day Message (1 or more days, e.g. holiday)'
        verbose_name_plural = 'Calendar Full Day Messages (1 or more days, e.g. holiday)'
    
    
class ScheduledBannerMessage(CalendarEvent):
    def get_display_msg(self):
        return self.display_name
        
    class Meta:
        verbose_name = 'Scheduled Banner Message (Displayed over calendar)'
        verbose_name_plural = 'Scheduled Banner Messages (Displayed over calendar)'
