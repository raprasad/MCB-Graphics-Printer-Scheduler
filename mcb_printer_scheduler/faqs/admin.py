from django.contrib import admin
from faqs.models import FAQCategory, FrequentlyAskedQuestion


class FAQCategoryAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display= ('name', 'sort_order') 
    list_editable = ('sort_order',)
admin.site.register(FAQCategory, FAQCategoryAdmin)


class FrequentlyAskedQuestionAdmin(admin.ModelAdmin):
    save_on_top = True
    readonly_fields = ('id_hash', 'created', 'last_update')
    list_display= ('question', 'category', 'sort_order', 'is_visible', 'last_update')
    list_filter = ('is_visible', 'category',)
    search_fields = ( 'question', 'answer', 'category__name',)
admin.site.register(FrequentlyAskedQuestion, FrequentlyAskedQuestionAdmin)
