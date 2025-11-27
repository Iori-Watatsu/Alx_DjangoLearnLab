from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, AuthorSummarySerializer


@api_view(['GET'])
def api_root(request, format=None):

    return Response({
        'authors': reverse('author-list', request=request, format=format),
        'books': reverse('book-list', request=request, format=format),
        'message': 'Advanced API Project - Custom Serializers Demo'
    })

class AuthorListView(generics.ListCreateAPIView):

    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSummarySerializer


class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer


class BookListView(generics.ListCreateAPIView):

    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all().prefetch_related('books')

    def get_serializer_class(self):

        if self.action == 'list':
            return AuthorSummarySerializer
        return AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer