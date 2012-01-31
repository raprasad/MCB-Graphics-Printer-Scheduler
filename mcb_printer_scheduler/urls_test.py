from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mcb_printer_scheduler.views.home', name='home'),
    # url(r'^mcb_printer_scheduler/', include('mcb_printer_scheduler.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^poster-printer/admin/', include(admin.site.urls)),
    
    url(r'^poster-printer/', include('mcb_printer_scheduler.schedule_viewer.urls')),
    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve'\
        , {'document_root': settings.MEDIA_ROOT }),
    
    
)
