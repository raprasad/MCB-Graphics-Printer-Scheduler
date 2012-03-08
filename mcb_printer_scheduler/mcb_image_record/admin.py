from django.contrib import admin
from mcb_image_record.models import ImageRecord
from mcb_image_record.forms import ImageRecordAdminForm

class ImageRecordAdmin(admin.ModelAdmin):
    form = ImageRecordAdminForm
    save_on_top = True
    list_display= ('name', 'thumb_view', 'created', 'last_update', )
    search_fields = ( 'name',)
    readonly_fields = ('created', 'last_update', 'thumb_image', 'thumb_view', 'main_view', )
    fieldsets = [
        ('', { 'fields':  [  'calendar_event', 'name', ('thumb_view', 'thumb_image'), 'main_image', 'main_view',   'notes', 'created', 'last_update' ]}), ]
admin.site.register(ImageRecord, ImageRecordAdmin)

