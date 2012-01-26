from django.conf.urls.defaults import *


urlpatterns = patterns(
    'schedule_viewer.views_signup'
    
#,    url(r'p/(?P<page_id>\d{1,7})/$', 'view_subpage', name='view_page_by_id')
#,    url(r'p/(?P<page_slug>(-|\w|_){1,150})/$', 'view_page_by_slug', name='view_page_by_slug')
,    url(r'$', 'view_signup_form', name='view_signup_form')
,
    
)
