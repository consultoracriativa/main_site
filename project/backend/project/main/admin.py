from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import ContentCategory, ContentContent
from .resources import ContentResource


class ContentAdmin(ImportExportModelAdmin):
    change_list_template = 'admin/main/ContentContent/change_list.html'
    base_site_template = 'admin/main/base_site.html'

    resource_class = ContentResource
    list_display = (
        'title',
        'category',
        'order',
        'active',
    )
    list_filter = ('category', )
    search_fields = (
        'title',
    )
    ordering = ('title', )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'text_show',
        'show_on_menu',
        'order',
        'active',
    )
    search_fields = (
        'category',
    )
    ordering = ('category', )


admin.site.register(ContentCategory, CategoryAdmin)
admin.site.register(ContentContent, ContentAdmin)
# admin.site.register(ContentContent, ContentResource)
