from django.contrib import admin
from .models import Author, Blog


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'age', 'email', 'github', 'linkedin')
    search_fields = ('full_name', 'email')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_active')
    search_fields = ('title', 'author__full_name')
    list_filter = ('is_active', 'created_at')
