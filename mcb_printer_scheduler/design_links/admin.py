from django.contrib import admin
from design_links.models import Organization, DesignLinkBase, DesignImage, DesignLink
from design_links.forms import DesignImageAdminForm



class DesignImageAdminInline(admin.TabularInline):
    model = DesignImage
    form = DesignImageAdminForm
    readonly_fields = ('thumb_view',)
    list_editable = ('sort_field',)
    fields = ('name', 'sort_field', 'description', 'main_image', 'thumb_view',)
    extra=0

class DesignLinkAdminInline(admin.TabularInline):
    model = DesignLink
    form = DesignImageAdminForm
    readonly_fields = ('view_link',)
    list_editable = ('sort_field',)
    fields = ('name', 'sort_field', 'description', 'design_link', 'view_link',)
    extra=0


class OrganizationAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = (DesignImageAdminInline, DesignLinkAdminInline)
    list_display= ('name', 'abbreviation', 'sort_field', 'is_visible', 'is_primary')
    search_fields = ( 'name',)
    list_filter = ('is_visible', 'is_primary')   
    readonly_fields = ('created', 'last_update',)
    list_editable = ('sort_field',)
admin.site.register(Organization, OrganizationAdmin)


class DesignLinkBaseAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display= ('organization', 'name', 'link_type', 'sort_field', 'description','created', 'last_update',  )
    search_fields = ( 'name', 'description')
    list_editable = ('sort_field',)
    
    readonly_fields = ('created', 'last_update', 'link_type', )
admin.site.register(DesignLinkBase, DesignLinkBaseAdmin)
    
class DesignImageAdmin(admin.ModelAdmin):
    form = DesignImageAdminForm
    save_on_top = True
    list_display= ('organization', 'name', 'thumb_view', 'sort_field','created', 'last_update', )
    search_fields = ( 'name', 'description')
    list_editable = ('sort_field',)
    
    readonly_fields = ('created', 'last_update', 'thumb_image', 'thumb_view', 'main_view', 'link_type',  )
    fieldsets = [
        ('', { 'fields':  [  'organization', 'name', 'description', ('thumb_view', 'thumb_image'), 'main_image', 'main_view', 'link_type', 'created', 'last_update' ]}), ]
admin.site.register(DesignImage, DesignImageAdmin)


class DesignLinkAdmin(admin.ModelAdmin):
    form = DesignImageAdminForm
    save_on_top = True
    list_display= ('organization', 'name', 'view_link', 'sort_field','created', 'last_update', )
    search_fields = ( 'name', 'description')
    list_editable = ('sort_field',)
    
    readonly_fields = ('created', 'last_update', 'view_link',  'link_type', )
admin.site.register(DesignLink, DesignLinkAdmin)

