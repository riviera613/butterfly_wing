from django.contrib import admin
from api.models import Post, Comment

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content", "username", "create_time")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post_id", "content", "username", "create_time")