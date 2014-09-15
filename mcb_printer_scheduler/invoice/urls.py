from django.conf.urls.defaults import *


urlpatterns = patterns(
    'reservation_history.views'

,    url(r'user-history/(?P<id_hash>(\w){32,40})/$', 'view_reservation_history', name='view_reservation_history')
,    url(r'create-invoice/(?P<res_id>[0-9]+)/$', 'view_create_invoice', name='view_create_invoice')
,    url(r'preview-invoice/(?P<res_id>[0-9]+)/$', 'view_preview_invoice', name='view_preview_invoice')
,
)
