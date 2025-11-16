from django.shortcuts import render,
from django.views.generic import DetailView,
from .models import Book,
from .models import Library

# Create your views here.
def home(request):
    return render(request, 'home.html')

# Func-Based View
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-Based View
from django.views.generic.detail import DetailView

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

