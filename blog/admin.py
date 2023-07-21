from django.contrib import admin
import csv
from django.http import HttpResponse

from .models import Post, User, Category, Tags, Comment
from import_export.admin import ImportExportModelAdmin
# from .import export_as_csv_action

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export Selected" 

@admin.register(User)
class webuser(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['username', 'email', 'city', 'address', 'phone_number']
    search_fields = ['username']
    list_filter = ['email']
    actions = ["export_as_csv"]
    

@admin.register(Post)
class webpost(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['author', 'title', 'published_date', 'category']
    search_fields = ['title']
    list_filter = ['published_date']
    filter_horizontal = ['tags']
    autocomplete_fields = ['category', 'author']
    actions = ["export_as_csv"]


admin.site.register(Category,CategoryAdmin)

@admin.register(Tags)
class webtags(ImportExportModelAdmin):
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Comment)
class webcomment(ImportExportModelAdmin):
    search_fields = ['email']
    list_filter = ['name']


