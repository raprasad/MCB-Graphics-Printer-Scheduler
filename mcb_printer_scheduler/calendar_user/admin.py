from django.contrib import admin
from calendar_user.models import CalendarUser

class CalendarUserAdmin(admin.ModelAdmin):
    save_on_top = True
    readonly_fields = ('last_name', 'first_name')
    list_display= ('user', 'last_name', 'first_name', 'is_calendar_admin',  'contact_email', 'phone_number', 'lab_name')
    list_filter = ('is_calendar_admin', )
    search_fields = ( 'user__username', 'user__last_name', 'user__first_name',  'contact_email', 'phone_number', )
admin.site.register(CalendarUser, CalendarUserAdmin)
