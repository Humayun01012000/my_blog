from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'user', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('user', 'created_at')  # Add filtering by user
    search_fields = ('title', 'content', 'user__username')  # Allow searching by user
