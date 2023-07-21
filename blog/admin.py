from django.contrib import admin
from .models import Post, User, Category, Tags, Comment
from import_export.admin import ImportExportModelAdmin


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']

@admin.register(User)
class webuser(ImportExportModelAdmin):
    list_display = ['username', 'email', 'city', 'address', 'phone_number']
    search_fields = ['username']
    list_filter = ['email']

    

@admin.register(Post)
class webpost(ImportExportModelAdmin):
    list_display = ['author', 'title', 'published_date', 'category']
    search_fields = ['title']
    list_filter = ['published_date']
    filter_horizontal = ['tags']
    autocomplete_fields = ['category', 'author']


admin.site.register(Category,CategoryAdmin)

@admin.register(Tags)
class webtags(ImportExportModelAdmin):
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Comment)
class webcomment(ImportExportModelAdmin):
    search_fields = ['email']
    list_filter = ['name']




