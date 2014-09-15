from django.conf.urls.defaults import *
from wkhtmltopdf.views import PDFTemplateView


urlpatterns = patterns(
    'reservation_history.views'

,    url(r'user-history/(?P<id_hash>(\w){32,40})/$', 'view_reservation_history', name='view_reservation_history')
,    url(r'create-invoice/(?P<res_id>[0-9]+)/$', 'view_create_invoice', name='view_create_invoice')
,    url(r'preview-invoice/(?P<res_id>[0-9]+)/$', 'view_preview_invoice', name='view_preview_invoice')
,    url(r'mark-status/(?P<res_id>[0-9]+)/(?P<status>(\w){1,12})/$', 'view_mark_status', name='view_mark_status')
,    url(r'mark-timeslot-free/(?P<res_id>[0-9]+)/(?P<status>(\w){1,5})/$', 'view_mark_timeslot_free', name='view_mark_timeslot_free')
,    url(r'display-invoice/(?P<invoice_no>(\w){10})/$', 'view_display_invoice', name='view_display_invoice')

)
