from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Book
from .serializers import BookSerializer, UserSerializer
from rest_framework import status
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=none):
    return Response({
        'books': reverse('book-list', request=request, format=format),
        'books_all': reverse('book-all-list', request=request, format=format),
        'token_obtain': reverse('api-token-obtain', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
        'message': 'Welcome to the Books API!'
    })
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
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_books(self, request):
        my_books = Book.objects.filter(created_by=request.user)
        serializer = self.get_serializer(my_books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def admin_books(self, request):
        all_books = Book.objects.all()
        serializer = self.get_serializer(all_books, many=True)
        return Response({
            'message': 'Admin access granted',
            'books': serializer.data
        })

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
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

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]