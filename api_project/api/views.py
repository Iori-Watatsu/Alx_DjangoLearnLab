from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Book
from .serializers import BookSerializer
from rest_framework import status

@api_view(['GET'])
def api_root(request, format=None):
    
    return Response({
        'books': reverse('book-list', request=request, format=format),
        'books_all': reverse('book-all-list', request=request, format=format),
        'message': 'Welcome to the Books API!'
    })

class BookList(generics.ListCreateAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'])
    def recent_books(self, request):

        recent_books = Book.objects.filter(publication_year__gte=1924)
        serializer = self.get_serializer(recent_books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def set_publication_year(self, request, pk=None):

        book = self.get_object()
        year = request.data.get('publication_year')
        if year:
            book.publication_year = year
            book.save()
            serializer = self.get_serializer(book)
            return Response(serializer.data)
        else:
            return Response(
                {'error': 'Publication year is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        