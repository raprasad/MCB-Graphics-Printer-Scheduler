from django.conf.urls.defaults import *


urlpatterns = patterns(
    'reservation_signup.views'

,    url(r'reserve/(?P<selected_date>\d{4}-\d{1,2}-\d{1,2})/$', 'view_signup_page', name='view_signup_page')

,    url(r'reservation-complete/(?P<id_hash>(\w){32,40})/$', 'view_signup_page_success', name='view_signup_page_success')

,
)

urlpatterns += patterns(
    'reservation_signup.view_cancel'
,    url(r'email/(?P<id_hash>(\w){32,40})/$', 'view_code_reminder', name='view_code_reminder')

,
    
)

urlpatterns += patterns(
    'reservation_signup.view_cancel'
,    url(r'cancel/(?P<id_hash>(\w){32,40})/$', 'view_cancel_signup', name='view_cancel_signup')

,    url(r'reservation-cancelled/(?P<id_hash>(\w){32,40})/$', 'view_cancel_success', name='view_cancel_success')

,
    
)
