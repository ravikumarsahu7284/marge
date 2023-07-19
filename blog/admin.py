from django.contrib import admin
from .models import Post, User, Category, Tags, Comment


admin.site.register(Post)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(Comment)


