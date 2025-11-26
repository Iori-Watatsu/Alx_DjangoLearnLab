from django.urls import path, include
from . import views
from rest_framework.routers improt DefaultRouter
from .views import Booklist, api_root, BookViewSet, UserViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.refister(r'books_all', BookViewSet, basename='book-all')
router.register(r'users', UserViewSet, basename='user')

app_name = 'api'

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('books/', views.BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('', include(router.urls)),
    path('token/', obtain_auth_token, name='api-token-obtain')
]