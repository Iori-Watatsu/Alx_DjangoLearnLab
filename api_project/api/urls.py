from django.urls import path, include
from . import views
from rest_framework.routers improt DefaultRouter
from .views import Booklist, api_root, BookViewSet

router = DefaultRouter()
router.refister(r'books_all', BookViewSet, basename='book-all')

app_name = 'api'

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('books/', views.BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('', include(router.urls)),
]