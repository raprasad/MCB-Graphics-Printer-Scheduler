from django.contrib import admin
from reservation_type.models import DayOfWeek, ReservationType
from reservation_type.forms import ReservationTypeForm

class DayOfWeekAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('day', 'day_number', )
admin.site.register(DayOfWeek, DayOfWeekAdmin)

class ReservationTypeAdmin(admin.ModelAdmin):
    form = ReservationTypeForm
    save_on_top = True
    readonly_fields = ('available_days_of_week', 'created', 'last_update')
    list_display= ('name', 'is_default', 'is_active', 'opening_time', 'closing_time','start_date', 'end_date', 'available_days_of_week',  'created', 'last_update', )
    filter_horizontal = ('days_allowed',)
    list_filter = ( 'is_default', 'is_active', )
    search_fields = ( 'name', )
admin.site.register(ReservationType, ReservationTypeAdmin)
