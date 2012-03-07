from django.contrib import admin
from mcb_image_record.models import ImageRecord

class ImageRecordAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display= ('name', 'created', 'last_update', )
    search_fields = ( 'name',)
    readonly_fields = ('created', 'last_update', )
admin.site.register(ImageRecord, ImageRecordAdmin)
