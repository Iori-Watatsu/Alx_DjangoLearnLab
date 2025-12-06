from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from django.contrib.auth.views import LogoutView

app_name = 'blog'

urlpatterns = [
    # Home and about
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # Posts
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/update/', views.post_update, name='post_update'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('posts/<int:pk>/like/', views.post_like, name='post_like'),

    # Post by date
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.post_detail, name='post_detail_date'),

    # Categories and tags
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    path('author/<str:username>/', views.author_posts, name='author_posts'),

    # Comments
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),

    # User management
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Search
    path('search/', views.search, name='search'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Blog Post URLs
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    # Home page (can be post list or custom home)
    path('', PostListView.as_view(), name='home'),
]