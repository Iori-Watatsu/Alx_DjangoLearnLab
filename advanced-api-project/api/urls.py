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

    path('', include(router.urls)),
]