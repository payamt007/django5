from django.contrib import admin
from .models import Feed, Post


class FeedAdmin(admin.ModelAdmin):
    fields = ["title", "link", "user"]
    list_display = ["title", "user"]


class PostAdmin(admin.ModelAdmin):
    fields = ["title", "link", "description", "feed", "read", "followed"]
    list_display = ["title", "link", "pubDate"]


admin.site.register(Feed, FeedAdmin)
admin.site.register(Post, PostAdmin)
