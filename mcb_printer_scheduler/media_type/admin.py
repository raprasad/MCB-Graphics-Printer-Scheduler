from django.contrib import admin
from media_type.models import PrintMediaType


class PrintMediaTypeAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display= ('name', 'sort_order', 'available',)
    search_fields = ( 'name',)
    list_editable = ('sort_order',)
    list_filter = ('available',)
admin.site.register(PrintMediaType, PrintMediaTypeAdmin)
