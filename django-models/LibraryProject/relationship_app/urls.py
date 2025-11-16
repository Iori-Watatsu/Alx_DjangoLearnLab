from django.urls import path
from . import views
from .views import list_books

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail')

    # Auth Views
    path('login/', views.user.login, name='login'),
    path('logout/', views.user.login, name='logout'),
    path('register/', views.user.login, name='register'),
]
