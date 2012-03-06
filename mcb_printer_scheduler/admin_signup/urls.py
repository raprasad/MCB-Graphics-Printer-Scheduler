from django.conf.urls.defaults import *


# Set Reservation for another user
urlpatterns = patterns(
    'admin_signup.views'

,    url(r'reserve/(?P<selected_date>\d{4}-\d{1,2}-\d{1,2})/$', 'view_admin_signup_page', name='view_admin_signup_page')

,    url(r'reservation-complete/(?P<id_hash>(\w){32,40})/$', 'view_admin_signup_page_success', name='view_admin_signup_page_success')

,
)


# Set CalendarMessage events
urlpatterns += patterns(
    'admin_signup.views_blackout'

,    url(r'set-blackout-time/(?P<selected_date>\d{4}-\d{1,2}-\d{1,2})/$', 'view_blackout_signup_page', name='view_blackout_signup_page')
    
,    url(r'cal-msg-complete/(?P<id_hash>(\w){32,40})/$', 'view_blackout_signup_success', name='view_blackout_signup_success')

# ajax calls
,    url(r'get-valid-end-times/(?P<selected_date>\d{4}-\d{1,2}-\d{1,2})/$', 'get_valid_end_times', name='get_valid_end_times_base')
,    url(r'get-valid-end-times/(?P<selected_date>\d{4}-\d{1,2}-\d{1,2})/(?P<selected_time>\d{1,2}-\d{1,2})/$', 'get_valid_end_times', name='get_valid_end_times')

,
)


# Cancel CalendarMessage events
urlpatterns += patterns(
    'admin_signup.views_cancel'
,    url(r'cancel-calendar-message/(?P<id_hash>(\w){32,40})/$', 'view_cancel_calendar_message', name='view_cancel_calendar_message')

,    url(r'calendar-message-cancelled/(?P<id_hash>(\w){32,40})/(?P<selected_date>\d{4}-\d{1,2}-\d{1,2})/$', 'view_cancel_calendar_message_success', name='view_cancel_calendar_message_success')

,
    
)

