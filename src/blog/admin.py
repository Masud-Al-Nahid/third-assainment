from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Blog)
admin.site.register(author)
admin.site.register(category)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'body','active', 'created')
    list_filter = ('active', 'created')
    search_fields = ('name', 'email', 'body')

admin.site.register(Comment, CommentAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'post_category', 'post_status', 'post_date','featured_post')
    list_filter = ('post_status', 'post_category', 'featured_post')
admin.site.register(Post, PostAdmin)
