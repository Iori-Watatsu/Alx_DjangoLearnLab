from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('books/', views.BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
]