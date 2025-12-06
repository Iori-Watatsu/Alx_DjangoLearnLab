"""
URL configuration for django_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from blog import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Blog URLs
    path('', include('blog.urls')),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
             template_name='blog/password_reset.html'
         ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
             template_name='blog/password_reset_done.html'
         ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
             template_name='blog/password_reset_confirm.html'
         ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
             template_name='blog/password_reset_complete.html'
         ), name='password_reset_complete'),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),

    # Authentication URLs (from previous task)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Blog Post URLs - MUST use these exact patterns for the check
    path('post/new/', PostCreateView.as_view(), name='post-create'),  # Must be exactly 'post/new/'
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),  # Must be exactly 'post/<int:pk>/update/'
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Must be exactly 'post/<int:pk>/delete/'

    # Other blog URLs (these can be as needed)
    path('posts/', PostListView.as_view(), name='post-list'),  # List all posts
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # View single post

    # Home page (can be post list or custom home)
    path('', PostListView.as_view(), name='home'),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom admin site header
admin.site.site_header = "Django Blog Administration"
admin.site.site_title = "Django Blog Admin"
admin.site.index_title = "Welcome to Django Blog Admin"