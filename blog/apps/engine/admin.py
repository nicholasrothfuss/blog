from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'published_at'
    filter_horizontal = ('categories',)
    list_display = ('title', 'author', 'status', 'published_at', 'updated_at')
    list_filter = ('status', 'published_at', 'updated_at')
    ordering = ('-updated_at',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        return super().save_model(request, obj, form, change)
