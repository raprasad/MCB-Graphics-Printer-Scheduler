from django.conf.urls.defaults import *


urlpatterns = patterns(
    'design_links.views'

,    url(r'listing/$', 'view_logo_listing', name='view_logo_listing')

,
)
