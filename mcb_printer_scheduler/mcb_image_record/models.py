import os
import Image

from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime, timedelta
from calendar_event.models import CalendarEvent
try:
    from hashlib import sha1
except:
    import md5

'''
from mcb_image_record.models import *
r = ImageRecord.objects.all()[0]
im = Image.open(r.main_image.path)
im.size
(888, 724)
'''

MAX_MAIN_IMAGE_WIDTH = 500
MAX_THUMB_IMAGE_WIDTH = 100

class ImageRecord(models.Model):
    def get_image_upload_base(self):
        return os.path.join('mcb_images')#, 'month_%s' % datetime.today().strftime('%Y_%m'))

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

    main_image = models.ImageField(max_length=255, upload_to='mcb_images/main/month_%Y_%m')

    thumb_image = models.ImageField(max_length=255,upload_to='mcb_images/thumb/month_%Y_%m', blank=True, null=True, help_text='auto-filled on save')
    
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name
        
    def set_hash_id(self): 
        try:
            self.id_hash =  sha1('%s%s' % (self.id, self.name)).hexdigest()
        except: #md5 is for old versions of python
            self.id_hash =  md5.new('%s%s' % (self.id,  self.name)).hexdigest()
    


    def save(self):    
        if self.id is None:
            super(ImageRecord, self).save()     

        # if main image is too big, resize it
        print 'self.main_image.path: %s' % self.main_image.path
        print 'self.main_image.file: %s' % self.main_image.file
        """
        REPLACE WITH POST SAVE
        if self.main_image.width > MAX_MAIN_IMAGE_WIDTH or self.main_image.height > MAX_MAIN_IMAGE_WIDTH:
            print '1 - open it'
            im = Image.open(self.main_image.file.name)
            print '2- make thumb'
            im.thumbnail((MAX_MAIN_IMAGE_WIDTH, MAX_MAIN_IMAGE_WIDTH), Image.ANTIALIAS)
            print '3- save'
            im.save(self.main_image.file.name, quality=90)
        """  

        # make a thumbnail
        #thumb = Image.open(self.main_image.path)    # (1) open the main image
        #thumb = thumb.resize((MAX_THUMB_IMAGE_WIDTH, MAX_THUMB_IMAGE_WIDTH), Image.ANTIALIAS)
        #thumb_name = self.get_image_upload_directory_thumb(os.path.basename(self.main_image.name))
        #thumb.save(self.main_image.path, quality=100)
        
        self.set_hash_id()
    
        super(ImageRecord, self).save()    

    class Meta:
        ordering = ('name', '-created'  )

        