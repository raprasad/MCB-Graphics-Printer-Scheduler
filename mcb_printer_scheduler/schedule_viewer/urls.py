from django.conf.urls.defaults import *


urlpatterns = patterns(
    'schedule_viewer.views_calendar'
    
,    url(r'(?P<selected_month>\d{4}-\d{1,2})/$', 'view_month_calendar', name='view_month_calendar')
,    url(r'$', 'view_month_calendar', name='view_current_month_calendar')

,
    
)
