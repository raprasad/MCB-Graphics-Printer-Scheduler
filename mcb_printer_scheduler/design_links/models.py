import os
import Image

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime, timedelta
from django.db.models.signals import post_save      

 
try:
    from hashlib import sha1
except:
    import md5
    
MAX_LOGO_THUMB_IMAGE_DIM = 60
THUMB_UPLOAD_TO = os.path.join('logos', 'thumb')
MAIN_UPLOAD_TO = os.path.join('logos', 'main')
MAIN_NON_WEB_UPLOAD_TO = os.path.join('logos', 'main_nonweb')
'''
from design_links.models import *
for i in DesignImage.objects.all(): i.save()

'''
class Organization(models.Model):
    """
    School, Department, etc.
    """
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=20, unique=True, help_text='e.g. MCB, CSB, etc.')
    slug = models.SlugField(max_length=255, blank=True)

    website = models.URLField(blank=True, help_text='link to organization, not to logo')
    
    is_visible = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False, help_text='appear in top section of page')
    
    sort_field = models.IntegerField(default=10)
    
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def get_num_links(self):
        return DesignLinkBase.objects.filter(organization=self).count()
        
    def get_listing_links(self):
        lnks = []
        for l in DesignLinkBase.objects.filter(organization=self):
            if l.link_type == 'DesignLink':
                lnks.append(l.designlink)
            elif l.link_type == 'DesignImage':
                lnks.append(l.designimage)
            elif l.link_type == 'DesignImageNonWeb':
                lnks.append(l.designimagenonweb)
        return lnks
    
    def __unicode__(self):
        return '%s (%s)' % (self.name, self.abbreviation)
    
    class Meta:
        ordering = ('sort_field', 'abbreviation' )
        
        
class DesignLinkBase(models.Model):
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, help_text='optional: 1 sentence description')
    sort_field = models.IntegerField(default=10)

    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    link_type = models.CharField(max_length=25, blank=True)
    
    def __unicode__(self):
        return '%s - %s' % (self.name, self.organization.name)
            
    class Meta:
        verbose_name = 'All Logo/Image List'
        ordering = ('organization', 'sort_field', 'name' )
    
    
class DesignLink(DesignLinkBase):
    design_link = models.URLField(verify_exists=False)

    def save(self):
        self.link_type = self.__class__.__name__
        super(DesignLink, self).save()
        
    def view_link(self):
        if self.design_link:
            return '<a href="%s" target="_blank">%s</a>' % (self.design_link, self.design_link)
        return '(n/a)'
    view_link.allow_tags= True

    class Meta:
        verbose_name = 'Logo Image Link'
        
        
class DesignImage(DesignLinkBase):
    
    main_image = models.ImageField(max_length=255, upload_to=MAIN_UPLOAD_TO)

    thumb_image = models.ImageField(max_length=255, upload_to=THUMB_UPLOAD_TO,
      blank=True, null=True, help_text='auto-filled on save') #  'mcb_images/thumb/month_%Y_%m',

    def get_image_basename(self):
      
        if self.main_image and self.main_image.file:
            #print dir(self.main_image)
            return os.path.basename(str(self.main_image))
        return 'not available'
        
    def save(self):
        self.link_type = self.__class__.__name__
        super(DesignImage, self).save()

    def thumb_view(self):
        if self.thumb_image:
            return '<a href="%s"  target="_blank"><img src="%s" style="border:1px solid #333;" alt="thumb" /></a>' % (self.main_image.url, self.thumb_image.url)
        return '(n/a)'
        
    thumb_view.allow_tags= True

    def main_view(self):
        if self.main_image:
            return '<img src="%s" style="border:1px solid #333;"  target="_blank" alt="main" />' % (self.main_image.url)
        return '(n/a)'
    main_view.allow_tags= True
    
    def get_ext(self):
        if not self.main_image:
            return None
        try:
            return os.path.basename(self.main_image.path).split('.')[-1].upper()
        except:
            return None
        
    @staticmethod
    def update_image_sizes( sender, **kwargs):
        # if main image is too big, resize it; make a thumbnail image
        img_rec = kwargs.get('instance', None)
        if img_rec is None:
            return

        # (1) resize main image
        #if img_rec.main_image.width > MAX_MAIN_IMAGE_WIDTH or img_rec.main_image.height > MAX_MAIN_IMAGE_WIDTH:
        #    im = Image.open(img_rec.main_image.file.name)   # open image
        #    im.thumbnail((MAX_MAIN_IMAGE_WIDTH, MAX_MAIN_IMAGE_WIDTH), Image.ANTIALIAS) # resize
        #    im.save(img_rec.main_image.file.name, quality=90)   #save
        
        # (2) make a thumbnail
        thumb = Image.open(img_rec.main_image.file.name)    # open the main image
        thumb.thumbnail((MAX_LOGO_THUMB_IMAGE_DIM, MAX_LOGO_THUMB_IMAGE_DIM), Image.ANTIALIAS)

        thumb_full_dirname = os.path.join(settings.MEDIA_ROOT, THUMB_UPLOAD_TO)
        thumb_full_filename = os.path.join(thumb_full_dirname, os.path.basename(img_rec.main_image.path) )

        # if needed, make thumb directory
        if not os.path.isdir(thumb_full_dirname):
            os.makedirs(thumb_full_dirname)
        # save file
        ext = thumb_full_filename.split('.')[-1].lower()
        if ext not in ['gif', 'jpeg', 'jpg', 'png']:
            thumb_full_filename = thumb_full_filename.replace('.%s' % ext, '.jpg')
            thumb.save(thumb_full_filename, "JPEG", quality=100)
        else:
            thumb.save(thumb_full_filename, quality=100)
            
        # disconnect save signal, save the ImageRecord, and reconnect signal
        post_save.disconnect(DesignImage.update_image_sizes, sender=DesignImage)        
        # update/save django model
        img_rec.thumb_image.name = os.path.join(THUMB_UPLOAD_TO ,os.path.basename(thumb_full_filename)  ) 
        img_rec.save()
        
        post_save.connect(DesignImage.update_image_sizes, sender=DesignImage)
        
    class Meta:
        verbose_name = 'Logo Image File for Web (png, jpg, etc)'
        verbose_name_plural = verbose_name
    
post_save.connect(DesignImage.update_image_sizes, sender=DesignImage)
    

class DesignImageNonWeb(DesignLinkBase):

    image_file = models.FileField(max_length=255, upload_to=MAIN_NON_WEB_UPLOAD_TO)

    def get_image_basename(self):

      if self.image_file and self.image_file.file:
          #print dir(self.main_image)
          return os.path.basename(str(self.image_file))
      return 'not available'

    def save(self):
      self.link_type = self.__class__.__name__
      super(DesignImageNonWeb, self).save()

    def get_ext(self):
      if not self.image_file:
          return None
      try:
          return os.path.basename(self.image_file.path).split('.')[-1].upper()
      except:
          return None

    class Meta:
        verbose_name = 'Logo Image File Not-Web Ready (.ai, .eps, .psd etc)'
        verbose_name_plural = verbose_name


