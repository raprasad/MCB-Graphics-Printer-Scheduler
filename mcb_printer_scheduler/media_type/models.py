from django.db import models

class PrintMediaType(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='fabric ($9/sq ft)')
    available = models.BooleanField(default=True)
    sort_order = models.IntegerField()

    def __unicode__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ('sort_order', 'name',)