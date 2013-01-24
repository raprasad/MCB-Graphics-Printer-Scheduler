from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.localflavor.us.models import PhoneNumberField
from datetime import datetime, timedelta

from hashlib import sha1
    

class FAQCategory(models.Model):
    name = models.CharField(max_length=255)
    sort_order = models.IntegerField()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('sort_order', 'name'  )
        verbose_name = 'FAQ Category'
        verbose_name_plural = 'FAQ Categories'
        db_table = 'faq_category'
        
        
class FrequentlyAskedQuestion(models.Model):
    """
    Basic calendar event class
    """
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.ForeignKey(FAQCategory, on_delete=models.PROTECT)
    
    sort_order = models.IntegerField()
    is_visible = models.BooleanField('Event is Active and Visible',     default=True)

    id_hash = models.CharField(max_length=40, blank=True, help_text='Auto-fill on save')  

    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.question
    
    def set_hash_id(self): 
        self.id_hash =  sha1('%s%s' % (self.id, self.created)).hexdigest()
        
    def save(self, *args, **kwargs):    
        if self.id is None:
            super(FrequentlyAskedQuestion, self).save(*args, **kwargs)     
        
        self.set_hash_id()
    
        super(FrequentlyAskedQuestion, self).save(*args, **kwargs)     


    class Meta:
        ordering = ('category', 'sort_order', 'question'  )
        verbose_name = 'Frequently Asked Question'
        verbose_name_plural = '%ss' % verbose_name
        db_table = 'faq'
