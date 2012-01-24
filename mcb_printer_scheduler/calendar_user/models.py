from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from datetime import timedelta
from django.contrib.localflavor.us.models import PhoneNumberField
from django.core import urlresolvers
try:
    from hashlib import sha1
except:
    import md5
    
class CalendarUser(models.Model):
    """
    An extension of the Django user class 
    - includes the active directory attribute userPrincipalName
    """
    user = models.ForeignKey(User, unique=True)
    id_hash = models.CharField(max_length=40, blank=True, null=True, help_text='Auto-fill on save')   # 

    is_calendar_admin = models.BooleanField(default=False)
    
    phone_number = PhoneNumberField(blank=True)
    contact_mail = models.EmailField(max_length=150, blank=True)
    lab_name = models.CharField(max_length=100, blank=True)
    billing_code = models.CharField('33 digit code', max_length=39, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    
    
    def __unicode__(self):
        if self.user.last_name and self.user.first_name:
            return self.get_fullname_last_first()
            #return self.get_fullname()
            
        return str(self.user)

    def get_email(self):
        return self.user.email

    def last_name(self):
        return self.user.last_name

    def first_name(self):
            return self.user.first_name
        
    def get_lname(self):
        return self.user.last_name

    def get_fname(self):
        return self.user.first_name

    def get_first_initial_lastname(self):
        if not self.user.first_name:
            return self.user.last_name
        return '%s. %s' % (self.user.first_name[0], self.user.last_name)

    def get_fullname_last_first(self):
        return '%s, %s' % (self.user.last_name, self.user.first_name)

    def get_fullname(self):
        return '%s %s' % (self.user.first_name ,self.user.last_name)

    def save(self):
    
        if self.id == None:
            super(CalendarUser, self).save()        # Call the "real" save() method.
         
        # update the hash.  md5 is for old versions of python
        try:
            self.id_hash =  sha1('%s%s' % (self.id, self.user.username)).hexdigest()
        except:
            self.id_hash =  md5.new('%s%s' % (self.id, self.user.username)).hexdigest()
        
        # self.user.email directly from Harvard LDAP, contact_email may be different
        if not self.contact_email:
            self.contact_email = self.user.email
            
        super(LabUser, self).save()        # Call the "real" save() method.

    class Meta:
        ordering = ('user__last_name',  )

User.profile = property(lambda u: CalendarUser.objects.get_or_create(user=u)[0])
