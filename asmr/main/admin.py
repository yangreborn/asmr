from django.contrib import admin

from .models import Studio, Author


# Register your models here.
@admin.register(Studio)
class PageAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_over', 'add_time', 'edit_time']
    readonly_fields = ['add_time', 'edit_time']

@admin.register(Author)
class PageAdmin(admin.ModelAdmin):
    list_display = ['name', 'studio', 'description', 'is_over', 'country', 'type', 'is_cast', 'level', 'add_time', 'edit_time']
    readonly_fields = ['add_time', 'edit_time']
    list_filter = ['studio', 'name', 'country', 'type', 'is_cast', 'level']

    def save_model(self, request, obj, form, change):
        if obj.alias:
            obj.alias = obj.alias.replace('，', ',')
        super().save_model(request, obj, form, change)