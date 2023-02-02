from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('body')
    list_display = ('title', 'author', 'created_on', 'listed')
    search_fields = ['title', 'author', 'body']
    readonly_fields = ('likes', 'dislikes',)
    list_filter = ('created_on', 'listed')
    prepopulated_fields = {
        'slug': ('title',)
        }


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'commenter', 'created_on', 'parent', 'id')
    list_filter = ('created_on',)
    search_fields = ['post', 'commenter', 'body']