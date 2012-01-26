from django.contrib import admin
from calendar_event.models import CalendarEvent, Reservation, CalendarMessage, CalendarFullDayMessage, ScheduledBannerMessage
from calendar_event.forms import TimeCheckForm

class CalendarEventAdmin(admin.ModelAdmin):
    form = TimeCheckForm
    save_on_top = True
    list_display= ('display_name', 'start_time', 'end_time', 'is_visible')
    list_filter = ('is_visible', 'subclass_name',)
    search_fields = ( 'display_name',)
    readonly_fields = ('subclass_name',)
admin.site.register(CalendarEvent, CalendarEventAdmin)
admin.site.register(CalendarMessage, CalendarEventAdmin)
admin.site.register(CalendarFullDayMessage, CalendarEventAdmin)
admin.site.register(ScheduledBannerMessage, CalendarEventAdmin)


class ReservationAdmin(admin.ModelAdmin):
    form = TimeCheckForm
    save_on_top = True
    readonly_fields = ('subclass_name',)
    list_display= ('display_name', 'user', 'start_time', 'end_time', 'contact_email', 'contact_phone', 'lab_name', 'is_cancelled' )
    list_filter = ('is_visible', 'is_cancelled', 'user',)
    search_fields = ( 'display_name', 'user__last_name', 'user__first_name', 'lab', 'billing_code')
admin.site.register(Reservation, ReservationAdmin)


