from django.conf.urls.defaults import *


urlpatterns = patterns(
    'login.views'
,    url(r'logout/$', 'view_logout_page', name='view_logout_page')    

)

urlpatterns += patterns(
    'login.views_callback'
    ,    url(r'^callback/$', 'view_handle_pin_callback', name='view_handle_pin_callback' ),

)



