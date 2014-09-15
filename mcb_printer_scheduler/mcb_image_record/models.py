import os
from PIL import Image

from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save      
from django.conf import settings

from datetime import datetime, timedelta
from calendar_event.models import CalendarEvent, Status
from calendar_user.models import CalendarUser
try:
    from hashlib import sha1
except:
    import md5

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

'''
from mcb_image_record.models import *
r = ImageRecord.objects.all()[0]
im = Image.open(r.main_image.path)
im.size
(888, 724)
'''

MAX_MAIN_IMAGE_WIDTH = 600
MAX_THUMB_IMAGE_WIDTH = 140

class ImageRecord(models.Model):
    def get_image_upload_base(self):
        return os.path.join('mcb_images', 'month_%s' % datetime.today().strftime('%Y_%m'))

    def get_image_upload_directory(self, attname):
        return os.path.join(self.get_image_upload_base(), 'main', attname)

    def get_image_upload_directory_thumb(self, attname):
        return os.path.join(self.get_image_upload_base(), 'thumb', attname)
    
    """
    Store thumbnail records related to reservations
    """
    calendar_event = models.ForeignKey(CalendarEvent)       # Used general "CalendarEvent" in case of future subclass
    
    name = models.CharField(max_length=255, help_text='image description')
    id_hash = models.CharField(max_length=40, blank=True, help_text='Auto-fill on save')   # 

    main_image = models.ImageField(max_length=255, upload_to=get_image_upload_directory)#'mcb_images/main/month_%Y_%m')

    thumb_image = models.ImageField(max_length=255, upload_to=get_image_upload_directory_thumb,
    blank=True, null=True, help_text='auto-filled on save') #  'mcb_images/thumb/month_%Y_%m',
    
    notes = models.TextField(blank=True, help_text='optional')
    
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def thumb_view(self):
        if self.thumb_image:
            return '<a href="%s"><img src="%s" style="border:1px solid #333;" /></a>' % (self.main_image.url, self.thumb_image.url)
        return '(auto-filled when main image is uploaded)'
    thumb_view.allow_tags= True
    
    def main_view(self):
        if self.main_image:
            return '<img src="%s" style="border:1px solid #333;" />' % (self.main_image.url)
        return '(blank)'
    main_view.allow_tags= True

    def __unicode__(self):
        return self.name
        
    def set_hash_id(self): 
        try:
            self.id_hash =  sha1('%s%s' % (self.id, self.name)).hexdigest()
        except: #md5 is for old versions of python
            self.id_hash =  md5.new('%s%s' % (self.id,  self.name)).hexdigest()
    
    @staticmethod
    def update_image_sizes( sender, **kwargs):
        # if main image is too big, resize it; make a thumbnail image
        img_rec = kwargs.get('instance', None)
        if img_rec is None:
            return

        # (1) resize main image
        if img_rec.main_image.width > MAX_MAIN_IMAGE_WIDTH or img_rec.main_image.height > MAX_MAIN_IMAGE_WIDTH:
            im = Image.open(img_rec.main_image.file.name)   # open image
            im.thumbnail((MAX_MAIN_IMAGE_WIDTH, MAX_MAIN_IMAGE_WIDTH), Image.ANTIALIAS) # resize
            im.save(img_rec.main_image.file.name, quality=90)   #save
        
        # (2) make a thumbnail
        thumb = Image.open(img_rec.main_image.file.name)    # open the main image
        thumb.thumbnail((MAX_THUMB_IMAGE_WIDTH, MAX_THUMB_IMAGE_WIDTH), Image.ANTIALIAS)
        thumb_fullpath = os.path.join(settings.MEDIA_ROOT\
                        , img_rec.get_image_upload_directory_thumb(os.path.basename(img_rec.main_image.path)) )

        # if needed, make thumb directory
        if not os.path.isdir(os.path.dirname(thumb_fullpath)):
            os.makedirs(os.path.dirname(thumb_fullpath))
        # save file
        thumb.save(thumb_fullpath, quality=100)

        # disconnect save signal, save the ImageRecord, and reconnect signal
        post_save.disconnect(ImageRecord.update_image_sizes, sender=ImageRecord)        
        # update/save django model
        img_rec.thumb_image.name = img_rec.get_image_upload_directory_thumb(os.path.basename(thumb_fullpath))
        img_rec.save()
        post_save.connect(ImageRecord.update_image_sizes, sender=ImageRecord)
        
    def send_user_email(self):
        lu = {}
        cal_event = self.calendar_event
        
        try:
            self.calendar_event.status = Status.objects.get(name="received")
            self.calendar_event.save()
        except:
            raise

        #if cal_event.get_subclass_name() == "Reservation":
        
        #cal_user = CalendarUser.objects.get(pk=1)
        cal_user = self.calendar_event.reservation.user
        lu.update({'cal_event': cal_event, 'cal_user': cal_user})
        plaintext = get_template('email/received.txt')
        htmly     = get_template('email/received.html')
        d = Context(lu)
        subject, from_email, to = 'Your Poster has been uploaded', 'mcbgraphics@example.com', 'emattison@gmail.com'
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        #msg.send()

        filename = "/vagrant/MCB-Graphics-Printer-Scheduler/email_log/email%s.txt" % datetime.now().strftime("%y%m%d_%H%M")
        with open(filename, "w") as f:
            f.write(text_content)
            
    def save(self):    
        if self.id is None:
            super(ImageRecord, self).save()     
            self.send_user_email()

        self.set_hash_id()
    
        super(ImageRecord, self).save()    

    class Meta:
        ordering = ('name', '-created'  )
        db_table = 'mcb_image_record'
post_save.connect(ImageRecord.update_image_sizes, sender=ImageRecord)
