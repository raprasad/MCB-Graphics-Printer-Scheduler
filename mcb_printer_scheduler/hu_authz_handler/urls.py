from django.conf.urls.defaults import *


urlpatterns = patterns(
    'hu_authz_handler.views'
,    url(r'logout/$', 'view_logout_page', name='view_logout_page')    

)


urlpatterns += patterns(
    'hu_authz_handler.views_callback'
    ,    url(r'^callback/$', 'view_handle_authz_callback', name='view_handle_pin_callback' ),
    #,    url(r'^callback/$', 'view_handle_authz_callback', name='view_handle_authz_callback' ),

)



