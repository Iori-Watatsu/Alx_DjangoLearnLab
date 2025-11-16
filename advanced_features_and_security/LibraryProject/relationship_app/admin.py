from django.conf import settings
from django.contrib import admin
from .models import Library, Book, Librarian  # only register your real models

admin.site.register(Library)
admin.site.register(Book)
admin.site.register(Librarian)
# Register your models here.

