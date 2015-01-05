from django.contrib import admin
from calendar_event.models import CalendarEvent, Status, Reservation, CalendarMessage, CalendarFullDayMessageGroup,  CalendarFullDayMessage, ScheduledBannerMessage
from calendar_event.forms import TimeCheckForm
from mcb_image_record.models import ImageRecord
from mcb_image_record.forms import ImageRecordAdminForm


class ImageRecordAdminInline(admin.TabularInline):
    model = ImageRecord
    form = ImageRecordAdminForm
    readonly_fields = ('thumb_view',)
    fields = ('name', 'notes', 'main_image', 'thumb_view',)
    extra=0


class CalendarFullDayMessageGroupAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display= ('group_name', 'num_events','created', 'last_update', )
    search_fields = ( 'group_name',)
    readonly_fields = ('num_events', 'created', 'last_update', )
admin.site.register(CalendarFullDayMessageGroup, CalendarFullDayMessageGroupAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_order', 'hex_color')

class CalendarEventAdmin(admin.ModelAdmin):
    form = TimeCheckForm
    save_on_top = True
    inlines = (ImageRecordAdminInline,)
    list_display= ('display_name', 'start_datetime', 'end_datetime', 'status', 'is_visible')
    list_filter = ('is_visible', 'subclass_name', 'status', 'is_timeslot_free')
    search_fields = ( 'display_name',)
    readonly_fields = ('subclass_name',)
admin.site.register(CalendarEvent, CalendarEventAdmin)
admin.site.register(CalendarMessage, CalendarEventAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(CalendarFullDayMessage, CalendarEventAdmin)


class ReservationAdmin(admin.ModelAdmin):
    form = TimeCheckForm
    save_on_top = True
    inlines = (ImageRecordAdminInline,)
    readonly_fields = ('subclass_name',)
    list_display= ('display_name', 'user', 'include_poster_tube','start_datetime', 'end_datetime', 'contact_email', 'contact_phone', 'lab_name', 'status', 'is_cancelled', 'created' )
    list_filter = ('is_visible', 'is_cancelled', 'include_poster_tube', 'print_media', 'user',)
    search_fields = ( 'display_name', 'poster_tube_details', 'user__last_name', 'user__first_name', 'lab', 'billing_code', 'printing_media_details')
admin.site.register(Reservation, ReservationAdmin)


class ScheduledBannerMessageAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display= ('name', 'start_datetime', 'end_datetime', 'is_active', 'banner_message' )
    list_filter = ('is_active', )
    search_fields = ( 'name', 'banner_message',)
admin.site.register(ScheduledBannerMessage, ScheduledBannerMessageAdmin)

