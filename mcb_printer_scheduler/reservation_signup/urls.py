from django.conf.urls.defaults import *


urlpatterns = patterns(
    'reservation_signup.views'

,    url(r'reserve/(?P<selected_date>\d{4}-\d{1,2}-\d{1,2})/$', 'view_signup_page', name='view_signup_page')

,
    
)
