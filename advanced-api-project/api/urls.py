from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register ViewSets
router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet)
router.register(r'books', views.BookViewSet)

app_name = 'api'

urlpatterns = [

    path('', views.api_root, name='api-root'),

    path('authors-list/', views.AuthorListView.as_view(), name='author-list'),
    path('authors-list/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('books-list/', views.BookListView.as_view(), name='book-list'),
    path('books-list/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    path('authors/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'),
    path('authors/<int:pk>/delete/', views.AuthorDeleteView.as_view(), name='author-delete'),
    path('books/search/', views.BookSearchView.as_view(), name='book-search'),
    path('books/recent/', views.RecentBooksView.as_view(), name='recent-books'),

    path('viewset', include(router.urls)),
]

urlpatterns += [
    path('docs/', views.api_root, name='api-docs'),
]