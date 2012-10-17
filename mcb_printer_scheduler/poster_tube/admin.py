from django.contrib import admin
from poster_tube.models import PosterTubeColor, PosterTubeType



class PosterTubeColorAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display= ('name',)
    search_fields = ( 'name',)
admin.site.register(PosterTubeColor, PosterTubeColorAdmin)

class PosterTubeTypeAdmin(admin.ModelAdmin):
    save_on_top = True
    readonly_fields = ('colors',)
    list_display= ('name', 'price', 'available', 'colors',)
    search_fields = ( 'name',)
    list_filter = ('available',)
    filter_horizontal = ('color_choices',)
admin.site.register(PosterTubeType, PosterTubeTypeAdmin)
        
