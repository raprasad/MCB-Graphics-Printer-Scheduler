from django.conf.urls.defaults import *


urlpatterns = patterns(
    'login.views'
,    url(r'logout/$', 'view_logout_page', name='view_logout_page')    
)
