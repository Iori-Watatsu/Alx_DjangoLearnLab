"""
URL configuration for api_project project.

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
from django.urls import path, incldude
from django.http import HttpResponse

def home_view(request):

    return HttpResponse("""
    <html>
    <head>
    <title>Django REST Framework API Project</title>
    <style>
    body { font-family: Arial, sans-serif; margin: 40px; }
    h1 { color: #333; }
    ul { list-style-type: none; padding: 0; }
    li { margin: 10px 0; }
    a { text-decoration: none; color: #007bff; padding: 8px 16px; border: 1px solid #007bff; border-radius: 4px; display: inline-block; }
    a:hover { background-color: #007bff; color: white; }
    </style>
    </head>
    <body>
    <h1>Django REST Framework API Project</h1>
    <p>Server is running correctly!</p>
    <p>Available endpoints:</p>
    <ul>
    <li><a href="/api/">API Root</a></li>
    <li><a href="/api/books/">Books API</a></li>
    <li><a href="/admin/">Admin Panel</a></li>
    </ul>
    </body>
    </html>
    """)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', home_view, name='home'),
]
