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
    display_name = models.CharField(max_length=255)
    
    id_hash = models.CharField(max_length=40, blank=True, help_text='Auto-fill on save')   # 

    is_visible = models.BooleanField('Event is Active and Visible',     default=True)
    
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    
    subclass_name = models.CharField(max_length=70, blank=True, help_text='Event Type (auto-filled on save)')
    
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.display_name
    
    def get_event_length_in_minutes(self):
        if self.end_datetime is None or self.start_datetime is None:
            return None
        if self.end_datetime < self.start_datetime:
            return None
            
        time_diff = self.end_datetime - self.start_datetime
        return time_diff.seconds / 60
        
    def get_display_msg(self):
        if self.display_name:
            return self.display_name
            
        return '%s to %s' % (self.start_datetime.strftime('%I:%M%p')\
                    , self.end_datetime.strftime('%I:%M%p')) 
    
    def set_hash_id(self): 
        try:
            self.id_hash =  sha1('%s%s' % (self.id, self.start_datetime)).hexdigest()
        except: #md5 is for old versions of python
            self.id_hash =  md5.new('%s%s' % (self.id,  self.start_datetime)).hexdigest()
    
    def get_subclass_name(self):
        return self.__class__.__name__
    
    def save(self):    
        if self.id is None:
            super(CalendarEvent, self).save()     
        
        #self.display_name = self.get_display_msg()
        self.set_hash_id()
    
        super(CalendarEvent, self).save()    

    class Meta:
        ordering = ('-start_datetime', 'display_name'  )
        verbose_name = 'Calendar Event (view all events)'
        verbose_name_plural = 'Calendar Events (view all events)'
        db_table = 'cal_event'
        
        
class Reservation(CalendarEvent):
    user = models.ForeignKey(CalendarUser)
    contact_email = models.EmailField()
    lab_name = models.CharField('Lab or Group Affiliation', max_length=100, blank=True)
    billing_code = models.CharField('33 digit billing code', max_length=39, blank=True, help_text='optional, but will expedite paperwork')
    contact_phone = PhoneNumberField(help_text='To contact you regarding scheduling changes.')
    note = models.TextField(blank=True)
    is_cancelled = models.BooleanField(default=False)
    
    
    def is_reservation(self):
        """convenience for templates"""
        return True
        
    def get_display_msg(self):
        name = self.user.get_user_initials()
        if name is not None or not name.strip() == '':
            return name

        return self.user.getusername()
        
        #return '%s %s-%s' % (self.user.get_first_initial_lastname())\
        #                    , self.start_datetime.strftime('%I:%M%p')\
        #                    , self.end_datetime.strftime('%I:%M%p')) 
    

    def save(self):    
        if self.id is None:
            super(Reservation, self).save()     

        self.display_name = self.get_display_msg()
        self.set_hash_id()
    
        if self.is_cancelled:
            self.is_visible= False
        self.subclass_name = self.__class__.__name__
        super(Reservation, self).save()    
    
    
    class Meta:
        verbose_name = 'Reservation'
        db_table = 'cal_event_reservation'


class CalendarMessage(CalendarEvent):
    """For general messages, e.g. holidays, etc"""    
    def save(self):
        if self.id is None:
            super(CalendarMessage, self).save()     

        self.set_hash_id()

        self.subclass_name = self.__class__.__name__
        super(CalendarMessage, self).save()    

    def is_calendar_message(self):
        """convenience for templates"""
        return True
        
        
    class Meta:
        verbose_name = 'Calendar Message'
        verbose_name_plural = 'Calendar Messages'
        db_table = 'cal_event_msg'

class CalendarFullDayMessageGroup(models.Model):
    group_name = models.CharField(max_length=255)
    id_hash = models.CharField(max_length=40, blank=True, help_text='Auto-fill on save')  
    
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def get_calendar_full_days(self):
        return CalendarFullDayMessage.objects.filter(message_group=self, is_visible=True).order_by('start_datetime')
        
    def num_events(self):
        return CalendarFullDayMessage.objects.filter(message_group=self).count()
        
    def set_hash_id(self): 
        try:
            self.id_hash =  sha1('%s%s' % (self.id, self.group_name)).hexdigest()
        except: #md5 is for old versions of python
            self.id_hash =  md5.new('%s%s' % (self.id,  self.group_name)).hexdigest()
    
    def save(self):
       if self.id is None:
           super(CalendarFullDayMessageGroup, self).save()    

       self.set_hash_id()
       super(CalendarFullDayMessageGroup, self).save()    

    class Meta:
        db_table = 'cal_event_msg_group'
        
class CalendarFullDayMessage(CalendarEvent):
    message_group = models.ForeignKey(CalendarFullDayMessageGroup)
    """For general messages, e.g. holidays, etc"""    

    def is_fullday_message(self):
        """convenience for templates"""
        return True

    def save(self):
        if self.id is None:
            super(CalendarFullDayMessage, self).save()    

        self.set_hash_id()

        # make the start/end times 24 hours
        self.start_datetime = datetime(self.start_datetime.year, self.start_datetime.month, self.start_datetime.day)
        self.end_datetime = datetime(self.end_datetime.year, self.end_datetime.month, self.end_datetime.day) + timedelta(days=1) + timedelta(microseconds=-1)
        if self.start_datetime > self.end_datetime:
            self.end_datetime = self.start_datetime + timedelta(days=1) + timedelta(microseconds=-1)
        self.subclass_name = self.__class__.__name__

        super(CalendarFullDayMessage, self).save()    

    class Meta:
        verbose_name = 'All Day Message'
        verbose_name_plural = 'All Day Messages'
        db_table = 'cal_event_day_msg'
    
    
class ScheduledBannerMessage(models.Model):
    name = models.CharField(max_length=255, help_text='for internal use, not displayed for public')

    banner_message = models.TextField()
    
    id_hash = models.CharField(max_length=40, blank=True, help_text='Auto-fill on save')   # 

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    is_active = models.BooleanField(default=True, help_text='Will be visible on appropriate dates')

    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ('-start_datetime',)
        verbose_name = 'Scheduled Banner Message'
        verbose_name_plural = 'Scheduled Banner Messages'
        db_table = 'cal_event_banner_msg'
