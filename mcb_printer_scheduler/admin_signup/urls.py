from django.conf.urls.defaults import *


urlpatterns = patterns(
    'admin_signup.views'

,    url(r'reserve/(?P<selected_date>\d{4}-\d{1,2}-\d{1,2})/$', 'view_admin_signup_page', name='view_admin_signup_page')

,    url(r'reservation-complete/(?P<id_hash>(\w){32,40})/$', 'view_admin_signup_page_success', name='view_admin_signup_page_success')

,
)
