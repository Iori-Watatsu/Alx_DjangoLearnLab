from django.contrib import admin
from .models import Category, Tag, Post, Comment, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['author', 'content', 'created_at']
    can_delete = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status',
                    'published_date', 'view_count', 'comment_count']
    list_filter = ['status', 'category', 'published_date', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    date_hierarchy = 'published_date'
    ordering = ['-published_date']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Metadata', {
            'fields': ('status', 'published_date', 'meta_title', 'meta_description')
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    inlines = [CommentInline]

    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comments'

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new post
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'content_preview',
                    'created_at', 'is_approved', 'is_reply']
    list_filter = ['is_approved', 'created_at', 'post']
    search_fields = ['content', 'author__username', 'post__title']
    list_editable = ['is_approved']
    actions = ['approve_comments', 'disapprove_comments']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

    def is_reply(self, obj):
        return obj.parent is not None
    is_reply.boolean = True
    is_reply.short_description = 'Is Reply'

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} comments approved.')
    approve_comments.short_description = "Approve selected comments"

    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} comments disapproved.')
    disapprove_comments.short_description = "Disapprove selected comments"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']
    readonly_fields = ['created_at']