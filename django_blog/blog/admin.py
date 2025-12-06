# blog/admin.py
from django.contrib import admin
from .models import Post, Comment, Tag  # Import Tag if using custom model
from taggit.models import Tag as TaggitTag  # If using django-taggit

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'tag_list')
    list_filter = ('date_posted', 'author', 'tags')
    search_fields = ('title', 'content', 'tags__name')
    date_hierarchy = 'date_posted'

    def tag_list(self, obj):
        return ", ".join(t.name for t in obj.tags.all())
    tag_list.short_description = 'Tags'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'updated_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'post__title')
    date_hierarchy = 'created_at'

# Only if using custom Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'post_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'

# If using django-taggit and want to customize admin
admin.site.unregister(TaggitTag)  # Unregister default taggit admin

@admin.register(TaggitTag)
class TaggitTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    ordering = ('name',)