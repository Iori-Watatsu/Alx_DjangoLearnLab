from django.shortcuts import render
from rest_framework import generics, viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer, AuthorSummarySerializer
#from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Q

class BookPagination(PageNumberPagination):

    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):

        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class AuthorPagination(PageNumberPagination):

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
def api_root(request, format=None):

    return Response({
        'authors': {
            'url': reverse('author-list', request=request, format=format),
            'filtering': '?name=<author_name>&has_books=true',
            'searching': '?search=<query>',
            'ordering': '?ordering=name,-created_at'
        },
        'books': {
            'url': reverse('book-list', request=request, format=format),
            'filtering': '?author=1&publication_year_min=2000&recent=true',
            'searching': '?search=harry+potter',
            'ordering': '?ordering=-publication_year,title'
        },
        'advanced_search': {
            'url': reverse('book-advanced-search', request=request, format=format),
            'parameters': '?q=<query>&author=<name>&year_min=2000&exact_title=true'
        },
        'recent_books': {
            'url': reverse('recent-books', request=request, format=format),
            'parameters': '?author=1&ordering=-publication_year'
        },
        'message': 'Advanced API Project - Enhanced with Filtering, Searching, and Ordering'
    })

class AuthorListView(generics.ListCreateAPIView):

    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSummarySerializer
    permission_classes = [AllowAny]
    pagination_class = AuthorPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = AuthorFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

class BookListView(generics.ListCreateAPIView):

    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]  # Allow anyone to view books
    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year', 'created_at']
    ordering = ['title']

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = BookFilter

    search_fields = [
        'title',
        'author__name',
        '=isbn',
    ]

    ordering_fields = [
        'title',
        'publication_year',
        'created_at',
        'updated_at',
        'author__name',
    ]
    ordering = ['title']

    def get_queryset(self):

        queryset = super().get_queryset()

        decade = self.request.query_params.get('decade')
        if decade and decade.isdigit():
            decade_start = int(decade)
            queryset = queryset.filter(
                publication_year__gte=decade_start,
                publication_year__lt=decade_start + 10
            )

        century = self.request.query_params.get('century')
        if century and century.isdigit():
            century_start = (int(century) - 1) * 100 + 1
            queryset = queryset.filter(
                publication_year__gte=century_start,
                publication_year__lt=century_start + 100
            )

        return queryset

    def list(self, request, *args, **kwargs):

        response = super().list(request, *args, **kwargs)

        response.data['query_metadata'] = {
            'filtering_options': {
                'exact_match': {
                    'author': 'Filter by exact author ID',
                    'publication_year': 'Filter by exact publication year',
                },
                'range_filters': {
                    'publication_year_min': 'Minimum publication year',
                    'publication_year_max': 'Maximum publication year',
                },
                'text_filters': {
                    'title': 'Filter by title (contains, case-insensitive)',
                    'author_name': 'Filter by author name (contains, case-insensitive)',
                },
                'multiple_value_filters': {
                    'publication_years': 'Comma-separated list of years (e.g., 1997,1998,1999)',
                },
                'custom_filters': {
                    'recent': 'true/false - Books from last 10 years',
                    'decade': 'Filter by decade (e.g., 1990 for 1990-1999)',
                    'century': 'Filter by century (e.g., 20 for 20th century)',
                }
            },
            'searching_options': {
                'search': 'Search across title, author name, and ISBN fields',
                'available_search_fields': ['title', 'author__name', 'isbn (exact)']
            },
            'ordering_options': {
                'ordering': 'Comma-separated fields (prefix with - for descending)',
                'available_ordering_fields': [
                    'title', '-title',
                    'publication_year', '-publication_year',
                    'created_at', '-created_at',
                    'author__name', '-author__name'
                ],
                'default_ordering': 'title'
            },
            'pagination_options': {
                'page': 'Page number',
                'page_size': 'Items per page (max: 100)'
            }
        }

        return response

    def get_queryset(self):

        queryset = super().get_queryset()

        # Filter by minimum publication year
        min_year = self.request.query_params.get('min_year')
        if min_year:
            queryset = queryset.filter(publication_year__gte=min_year)

        # Filter by maximum publication year
        max_year = self.request.query_params.get('max_year')
        if max_year:
            queryset = queryset.filter(publication_year__lte=max_year)

        return queryset

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Add related books by the same author
        related_books = Book.objects.filter(
            author=instance.author
        ).exclude(pk=instance.pk)[:5]
        related_serializer = BookSerializer(related_books, many=True)

        response_data = serializer.data
        response_data['related_books'] = related_serializer.data
        response_data['author_book_count'] = instance.author.books.count()

        return Response(response_data)

class BookCreateView(generics.CreateAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save()

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'Book created successfully',
                'book': serializer.data,
                'links': {
                    'detail': reverse('book-detail', args=[serializer.data['id']], request=request),
                    'list': reverse('book-list', request=request)
                }
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class BookUpdateView(generics.UpdateAPIView):

    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def perform_update(self, serializer):

        serializer.save()

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):

            instance._prefetched_objects_cache = {}

        return Response(
            {
                'message': 'Book updated successfully',
                'book': serializer.data,
                'changes': self.get_change_summary(instance, request.data)
            }
        )

    def get_change_summary(self, instance, new_data):

        changes = {}
        for field in ['title', 'publication_year', 'author']:
            old_value = getattr(instance, field)
            if field in new_data and str(new_data[field]) != str(old_value):
                changes[field] = {
                    'from': str(old_value),
                    'to': str(new_data[field])
                }
        return changes


class BookDeleteView(generics.DestroyAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        book_title = instance.title
        author_name = instance.author.name

        self.perform_destroy(instance)

        return Response(
            {
                'message': f'Book "{book_title}" by {author_name} has been successfully deleted.',
                'deleted_book': {
                    'title': book_title,
                    'author': author_name,
                    'publication_year': instance.publication_year
                }
            },
            status=status.HTTP_200_OK
        )

class AuthorListView(generics.ListAPIView):

    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSummarySerializer
    permission_classes = [AllowAny]
    pagination_class = AuthorPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'book_count', 'created_at']
    ordering = ['name']


class AuthorDetailView(generics.RetrieveAPIView):

    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

    class AuthorCreateView(generics.CreateAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'Author created successfully',
                'author': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class AuthorUpdateView(generics.UpdateAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class AuthorDeleteView(generics.DestroyAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]  # Only admins can delete authors

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        book_count = instance.books.count()

        if book_count > 0:
            return Response(
                {
                    'error': f'Cannot delete author "{instance.name}" because they have {book_count} book(s) associated. Please delete or reassign the books first.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        author_name = instance.name
        self.perform_destroy(instance)

        return Response(
            {
                'message': f'Author "{author_name}" has been successfully deleted.'
            },
            status=status.HTTP_200_OK
        )

class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all().prefetch_related('books')
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AuthorFilter
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):

        if self.action == 'list':
            return AuthorSummarySerializer
        return AuthorSerializer

class BookSearchView(generics.ListAPIView):

    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__name']

    def get_queryset(self):

        queryset = Book.objects.all().select_related('author')

        # Filter by publication decade
        decade = self.request.query_params.get('decade')
        if decade and decade.isdigit():
            decade_start = int(decade)
            queryset = queryset.filter(
                publication_year__gte=decade_start,
                publication_year__lt=decade_start + 10
            )

        # Filter by author name contains
        author_contains = self.request.query_params.get('author_contains')
        if author_contains:
            queryset = queryset.filter(author__name__icontains=author_contains)

        return queryset

    def list(self, request, *args, **kwargs):

        response = super().list(request, *args, **kwargs)

        # Add search metadata
        response.data['search_metadata'] = {
            'total_results': len(response.data),
            'search_filters_applied': {
                'decade': request.query_params.get('decade'),
                'author_contains': request.query_params.get('author_contains'),
                'search_query': request.query_params.get('search')
            },
            'available_filters': [
                'decade (e.g., 1990)',
                'author_contains (partial author name)',
                'search (title or author name)'
            ]
        }

        return response


class RecentBooksView(generics.ListAPIView):

    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        current_year = timezone.now().year
        recent_year = current_year - 20
        return Book.objects.filter(
            publication_year__gte=recent_year
        ).select_related('author').order_by('-publication_year')

    def list(self, request, *args, **kwargs):

        response = super().list(request, *args, **kwargs)

        current_year = timezone.now().year
        recent_year = current_year - 20

        response.data['metadata'] = {
            'description': f'Books published in the last 20 years (since {recent_year})',
            'total_recent_books': len(response.data),
            'year_range': f'{recent_year}-{current_year}'
        }

        return response


class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author__name', '=isbn']
    ordering_fields = ['title', 'publication_year', 'created_at', 'author__name']
    ordering = ['title']

    def get_serializer_class(self):
        if self.action == 'list':
            return AuthorSummarySerializer
        return AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BookPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author', 'publication_year']
    search_fields = ['title', 'author__name']

    @action(detail=False, methods=['get'])
    def recent(self, request):

        current_year = timezone.now().year
        recent_books = Book.objects.filter(
            publication_year__gte=current_year - 10
        )
        serializer = self.get_serializer(recent_books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def duplicate(self, request, pk=None):

        original_book = self.get_object()
        new_book = Book.objects.create(
            title=f"{original_book.title} (Copy)",
            author=original_book.author,
            publication_year=original_book.publication_year
        )
        serializer = self.get_serializer(new_book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BookFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        help_text="Filter by title (case-insensitive contains)"
    )

    publication_year_min = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        help_text="Filter by minimum publication year"
    )
    publication_year_max = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        help_text="Filter by maximum publication year"
    )

    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        help_text="Filter by author name (case-insensitive contains)"
    )

    publication_years = django_filters.BaseInFilter(
        field_name='publication_year',
        lookup_expr='in',
        help_text="Filter by specific publication years (comma-separated)"
    )

    recent = django_filters.BooleanFilter(
        method='filter_recent',
        help_text="Filter for recent books (published in last 10 years)"
    )

    def filter_recent(self, queryset, name, value):

        if value:
            current_year = timezone.now().year
            return queryset.filter(publication_year__gte=current_year - 10)
        return queryset

    class Meta:
        model = Book
        fields = {
            'author': ['exact'],
            'publication_year': ['exact', 'gte', 'lte'],
        }

class AuthorFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        help_text="Filter by author name (case-insensitive contains)"
    )

    has_books = django_filters.BooleanFilter(
        method='filter_has_books',
        help_text="Filter authors who have books"
    )

    def filter_has_books(self, queryset, name, value):

        if value:
            return queryset.filter(books__isnull=False).distinct()
        return queryset.filter(books__isnull=True)

    class Meta:
        model = Author
        fields = ['name']

class BookAdvancedSearchView(generics.ListAPIView):

    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    pagination_class = BookPagination

    def get_queryset(self):

        queryset = Book.objects.all().select_related('author')

        search_query = self.request.query_params.get('q')
        author_query = self.request.query_params.get('author')
        year_min = self.request.query_params.get('year_min')
        year_max = self.request.query_params.get('year_max')
        exact_title = self.request.query_params.get('exact_title')

        q_objects = Q()

        if search_query:
            if exact_title:

                q_objects &= Q(title__iexact=search_query)
            else:

                q_objects &= (
                    Q(title__icontains=search_query) |
                    Q(author__name__icontains=search_query)
                )

        if author_query:
            q_objects &= Q(author__name__icontains=author_query)

        if year_min:
            q_objects &= Q(publication_year__gte=year_min)
        if year_max:
            q_objects &= Q(publication_year__lte=year_max)

        return queryset.filter(q_objects).distinct()

def list(self, request, *args, **kwargs):

    response = super().list(request, *args, **kwargs)

    applied_filters = {
        'q': request.query_params.get('q'),
        'author': request.query_params.get('author'),
        'year_min': request.query_params.get('year_min'),
        'year_max': request.query_params.get('year_max'),
        'exact_title': request.query_params.get('exact_title'),
    }

    applied_filters = {k: v for k, v in applied_filters.items() if v is not None}

    response.data['search_metadata'] = {
        'applied_filters': applied_filters,
        'total_results': response.data['count'] if 'count' in response.data else len(response.data['results']),
        'search_parameters': {
            'q': 'Search query (searches title and author name)',
            'author': 'Filter by author name (contains)',
            'year_min': 'Minimum publication year',
            'year_max': 'Maximum publication year',
            'exact_title': 'true/false - Exact title match vs contains',
        }
    }

    return response

class RecentBooksView(generics.ListAPIView):

    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    pagination_class = BookPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['author']
    ordering_fields = ['publication_year', 'title']
    ordering = ['-publication_year']

    def get_queryset(self):

        current_year = timezone.now().year
        recent_year = current_year - 20

        queryset = Book.objects.filter(
            publication_year__gte=recent_year
        ).select_related('author')

        decade = self.request.query_params.get('decade')
        if decade and decade.isdigit():
            decade_start = int(decade)
            if decade_start >= recent_year // 10 * 10:  # Ensure it's within recent range
                queryset = queryset.filter(
                    publication_year__gte=decade_start,
                    publication_year__lt=decade_start + 10
                )

        return queryset

