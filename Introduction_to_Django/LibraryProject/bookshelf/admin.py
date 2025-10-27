from django.contrib import admin
from .models import Book

# Register your models here.

# Custom admin class
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns to show in the list view
    list_filter = ('author', 'publication_year')            # Filters on the right sidebar
    search_fields = ('title', 'author')                     # Searchable fields

# Register the Book model with the custom admin
admin.site.register(Book, BookAdmin)