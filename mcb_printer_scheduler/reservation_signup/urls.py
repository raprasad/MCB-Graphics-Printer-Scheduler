from django.conf.urls.defaults import *


urlpatterns = patterns(
    'reservation_signup.views'

,    url(r'reserve/(?P<selected_date>\d{4}-\d{1,2}-\d{1,2})/$', 'view_signup_page', name='view_signup_page')

,    url(r'success/(?P<id_hash>(\w){32,40})/$', 'view_signup_page_success', name='view_signup_page_success')



    
)
