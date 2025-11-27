"""
URL configuration for advanced_api_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    """
Simple home view to confirm the project is running.
    """
    return HttpResponse("""
<html>
<head>
<title>Advanced API Project</title>
<style>
body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
.container { max-width: 800px; margin: 0 auto; }
.endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #3498db; }
.endpoint h3 { margin-top: 0; color: #2c3e50; }
code { background: #e9ecef; padding: 2px 6px; border-radius: 3px; }
</style>
</head>
<body>
<div class="container">
<h1>Advanced API Project</h1>
<p>Welcome to the Advanced API Project with Custom Serializers!</p>

<h2>Available Endpoints:</h2>

<div class="endpoint">
<h3>API Root</h3>
<p><code>GET /api/</code> - List all available endpoints</p>
</div>

<div class="endpoint">
<h3>Authors (ViewSet)</h3>
<p><code>GET /api/authors/</code> - List all authors (summary)</p>
<p><code>POST /api/authors/</code> - Create a new author</p>
<p><code>GET /api/authors/{id}/</code> - Get author details with nested books</p>
<p><code>PUT /api/authors/{id}/</code> - Update author</p>
<p><code>DELETE /api/authors/{id}/</code> - Delete author</p>
</div>

<div class="endpoint">
<h3>Books (ViewSet)</h3>
<p><code>GET /api/books/</code> - List all books</p>
<p><code>POST /api/books/</code> - Create a new book</p>
<p><code>GET /api/books/{id}/</code> - Get book details</p>
<p><code>PUT /api/books/{id}/</code> - Update book</p>
<p><code>DELETE /api/books/{id}/</code> - Delete book</p>
</div>

<div class="endpoint">
<h3>Alternative Endpoints (Generic Views)</h3>
<p><code>GET /api/authors-list/</code> - List authors (alternative)</p>
<p><code>GET /api/books-list/</code> - List books (alternative)</p>
</div>

<div class="endpoint">
<h3>Admin</h3>
<p><code>GET /admin/</code> - Django admin interface</p>
</div>
</div>
</body>
</html>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api', include('api.urls')),
    path('', home_view, name='home'),
]
