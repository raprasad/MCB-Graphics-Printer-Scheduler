from django.conf.urls.defaults import *


urlpatterns = patterns(
    'faqs.views'
,    url(r'list/$', 'view_faqs', name='view_faqs')    

)
