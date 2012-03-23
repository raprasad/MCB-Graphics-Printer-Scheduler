from django.conf.urls.defaults import *


# Set Reservation for another user
urlpatterns = patterns(
    'admin_signup.views'

,    url(r'reserve/(?P<selected_date>\d{4}-\d{1,2}-\d{1,2})/$', 'view_admin_signup_page', name='view_admin_signup_page')

,    url(r'reservation-complete/(?P<id_hash>(\w){32,40})/$', 'view_admin_signup_page_success', name='view_admin_signup_page_success')

    # ajax calls
,    url(r'get-cal-user-contact-info/(?P<cal_user_id>\d{1,6})/$', 'get_cal_user_contact_info', name='get_cal_user_contact_info')

,    url(r'get-cal-user-contact-info/$', 'get_cal_user_contact_info', name='get_cal_user_contact_info_base')
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


# Set CalendarFullDayMessage events
urlpatterns += patterns(
    'admin_signup.views_blackout_days'

,    url(r'set-blackout-days/(?P<selected_date>\d{4}-\d{1,2}-\d{1,2})/$', 'view_blackout_days_signup_page', name='view_blackout_days_signup_page')

,    url(r'cal-blackout-days-complete/(?P<id_hash>(\w){32,40})/$', 'view_blackout_days_signup_success', name='view_blackout_days_signup_success')

    
)


# Cancel CalendarMessage events
urlpatterns += patterns(
    'admin_signup.views_cancel'
,    url(r'cancel-calendar-message/(?P<id_hash>(\w){32,40})/$', 'view_cancel_calendar_message', name='view_cancel_calendar_message')

,    url(r'calendar-message-cancelled/(?P<id_hash>(\w){32,40})/(?P<selected_date>\d{4}-\d{1,2}-\d{1,2})/$', 'view_cancel_calendar_message_success', name='view_cancel_calendar_message_success')

,
    
)

# Free Time Slot
urlpatterns += patterns(
    'admin_signup.views_free_timeslot'
,    url(r'free-timeslot/(?P<id_hash>(\w){32,40})/$', 'view_free_timeslot', name='view_free_timeslot')

)

# Adjust available times
urlpatterns += patterns(
    'admin_signup.views_adjust_time'
,    url(r'adjust-time-winow/(?P<selected_date>\d{4}-\d{1,2}-\d{1,2})/$', 'view_adjust_reservation_type', name='view_adjust_reservation_type')

,    url(r'adjust-time-winow-success/(?P<selected_date>\d{4}-\d{1,2}-\d{1,2})/$', 'view_adjust_reservation_type_success', name='view_adjust_reservation_type_success')


)


