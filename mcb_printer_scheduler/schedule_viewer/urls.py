from django.conf.urls.defaults import *


urlpatterns = patterns(
    'schedule_viewer.views_calendar'
    
#,    url(r'p/(?P<page_id>\d{1,7})/$', 'view_subpage', name='view_page_by_id')
#,    url(r'p/(?P<page_slug>(-|\w|_){1,150})/$', 'view_page_by_slug', name='view_page_by_slug')
,    url(r'(?P<selected_year>\d{4})-(?P<selected_month>\d{1,2})/$', 'view_month_calendar', name='view_month_calendar')
,    url(r'$', 'view_month_calendar', name='view_current_month_calendar')

,
    
)
