from django.contrib import admin
from invoice.models import Invoice

class InvoiceAdmin(admin.ModelAdmin):
    list_display= ('reservation', 'invoice_no', 'last_update', )
    readonly_fields = ('filename',)
    search_fields = ( 'invoice_no',)
admin.site.register(Invoice, InvoiceAdmin)
