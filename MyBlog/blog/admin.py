from django.contrib import admin

# Register your models here.
from blog.models import Post, UserFollowing, AlreadyRead


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date', 'id']
    list_filter = ['title', 'date']


@admin.register(UserFollowing)
class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ['user', 'following']


@admin.register(AlreadyRead)
class AlreadyReadAdmin(admin.ModelAdmin):
    list_display = ['user', 'post_id']