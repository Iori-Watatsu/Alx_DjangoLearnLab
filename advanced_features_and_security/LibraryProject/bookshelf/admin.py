from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

# Register your models here.

# Custom admin class
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns to show in the list view
    list_filter = ('author', 'publication_year')            # Filters on the right sidebar
    search_fields = ('title', 'author')                     # Searchable fields

# Register the Book model with the custom admin
admin.site.register(Book, BookAdmin)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin interface for the CustomUser model."""

    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'date_of_birth',
                'profile_photo'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'is_staff',
                'is_active'
            ),
        }),
    )