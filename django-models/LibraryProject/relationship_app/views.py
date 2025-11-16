from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Book, Library

# Create your views here.
def home(request):
    return render(request, 'home.html')

# Func-Based View
def list_books(request):
    books = Book.objects.all()
    return render(request, 'list_books.html', {'books': books})

# Class-Based View
from django.views.generic.detail import DetailView

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

