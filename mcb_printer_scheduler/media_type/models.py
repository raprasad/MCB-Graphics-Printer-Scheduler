from django.db import models
from decimal import Decimal

class PrintMediaType(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='fabric ($9/sq ft)')
    available = models.BooleanField(default=True)
    sort_order = models.IntegerField()
    dollar_cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __unicode__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ('sort_order', 'name',)
