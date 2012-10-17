from django.db import models

class PosterTubeColor(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        
class PosterTubeType(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    color_choices = models.ManyToManyField(PosterTubeColor)
    available = models.BooleanField(default=True)
    
    def get_color_options(self):
        if self.color_choices.count() == 0:
            return ''
        
        options = ','.join(map(lambda x: '"%s":"%s"' % (x.name, x.name), self.color_choices.all()))
        return '{%s}' % options
        
    def colors(self):
        if self.color_choices.count() == 0:
            return 'n/a'
        return '<br />'.join(map(lambda x: x.name, self.color_choices.all()))
    colors.allow_tags = True
    
    def __unicode__(self):
        return '%s ($%.2f)' % (self.name, self.price)

    class Meta:
        ordering = ('name',)