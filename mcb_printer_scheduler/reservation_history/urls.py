from django.conf.urls.defaults import *


urlpatterns = patterns(
    'reservation_history.views'

,    url(r'user-history/(?P<id_hash>(\w){32,40})/$', 'view_reservation_history', name='view_reservation_history')

,
)
