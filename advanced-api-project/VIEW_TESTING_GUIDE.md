# Custom and Generic Views Testing Guide

## Overview
This project demonstrates the implementation of custom views and generic views in Django REST Framework, showcasing different patterns for handling CRUD operations with proper permission controls.

## Generic Views Implemented

### Book Views
- **BookListView**: `GET /api/books/list/` - List all books (AllowAny)
- **BookDetailView**: `GET /api/books/{id}/` - Get book details (AllowAny)
- **BookCreateView**: `POST /api/books/create/` - Create new book (Authenticated)
- **BookUpdateView**: `PUT /api/books/{id}/update/` - Update book (Authenticated)
- **BookDeleteView**: `DELETE /api/books/{id}/delete/` - Delete book (Admin only)

### Author Views
- **AuthorListView**: `GET /api/authors/list/` - List all authors (AllowAny)
- **AuthorDetailView**: `GET /api/authors/{id}/` - Get author details (AllowAny)
- **AuthorCreateView**: `POST /api/authors/create/` - Create new author (Authenticated)
- **AuthorUpdateView**: `PUT /api/authors/{id}/update/` - Update author (Authenticated)
- **AuthorDeleteView**: `DELETE /api/authors/{id}/delete/` - Delete author (Admin only)

### Custom Views
- **BookSearchView**: `GET /api/books/search/` - Advanced book search with filters
- **RecentBooksView**: `GET /api/books/recent/` - Books from last 20 years

## Permission Structure

| View Type | Permission Class | Access Level |
|-----------|------------------|--------------|
| List/Detail | AllowAny | Public read access |
| Create/Update | IsAuthenticated | Authenticated users only |
| Delete | IsAdminUser | Admin users only |

## Testing with curl

### Public Endpoints (No authentication required)
```bash
# List all books
curl http://127.0.0.1:8000/api/books/list/

# Get specific book details
curl http://127.0.0.1:8000/api/books/1/

# Search books with filters
curl "http://127.0.0.1:8000/api/books/search/?search=harry&decade=1990"

# Get recent books
curl http://127.0.0.1:8000/api/books/recent/

# Create a new book (requires authentication)
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "title": "New Book Title",
    "author": 1,
    "publication_year": 2024
  }'

# Update a book (requires authentication)
curl -X PUT http://127.0.0.1:8000/api/books/1/update/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "title": "Updated Book Title",
    "publication_year": 2023
  }'

# Delete a book (requires admin user)
curl -X DELETE http://127.0.0.1:8000/api/books/1/delete/ \
  -u adminusername:adminpassword

# Filter by author
curl "http://127.0.0.1:8000/api/books/list/?author=1"

# Filter by publication year
curl "http://127.0.0.1:8000/api/books/list/?publication_year=1997"

# Search in title and author name
curl "http://127.0.0.1:8000/api/books/list/?search=tolkien"

# Order by publication year (descending)
curl "http://127.0.0.1:8000/api/books/list/?ordering=-publication_year"

# Combine multiple filters
curl "http://127.0.0.1:8000/api/books/list/?author=1&ordering=title&search=potter"

# Search by decade
curl "http://127.0.0.1:8000/api/books/search/?decade=1990"

# Search by author name contains
curl "http://127.0.0.1:8000/api/books/search/?author_contains=rowling"

# Combine search parameters
curl "http://127.0.0.1:8000/api/books/search/?search=harry&decade=1990"

Custom View Features
BookCreateView Enhancements

    Enhanced response with success message and links

    Proper validation error handling

    Custom perform_create method for additional logic

BookUpdateView Enhancements

    Change tracking and summary

    Support for partial updates

    Enhanced response format

BookDeleteView Enhancements

    Confirmation response with deleted book details

    Admin-only access restriction

    Custom destroy method

Testing Scenarios
1. Permission Testing

    Access read endpoints without authentication

    Attempt to create/update without authentication (should fail)

    Attempt to delete as regular user (should fail)

    Perform all operations as admin user

2. Validation Testing

    Try to create book with future publication year

    Attempt to create book with empty title

    Test duplicate book creation prevention

3. Filtering and Search Testing

    Test all available filter combinations

    Verify search functionality

    Test ordering options

    Verify pagination

View Configuration Documentation
Key Customizations

    Custom Pagination: Different page sizes for books and authors

    Advanced Filtering: DjangoFilterBackend with custom filters

    Search Integration: SearchFilter with configurable search fields

    Ordering Support: Multiple ordering options for list views

    Enhanced Responses: Custom response formats with metadata

    Permission Hierarchy: Tiered access control system

Method Overrides Used

    get_queryset(): Custom filtering logic

    list(): Enhanced response formatting

    create()/update()/destroy(): Custom success responses

    perform_create()/perform_update(): Custom save logic

Mixins and Base Classes

    generics.ListAPIView: Read-only list operations

    generics.RetrieveAPIView: Single object retrieval

    generics.CreateAPIView: Object creation

    generics.UpdateAPIView: Object updates

    generics.DestroyAPIView: Object deletion

text


## Step 5: Run Migrations and Test

Let's run the setup and test our views:

```bash
# Make sure you're in the advanced-api-project directory
cd advanced-api-project

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install new dependency
pip install django-filter

# Run migrations (if any model changes)
python manage.py makemigrations
python manage.py migrate

# Create a superuser for testing admin features
python manage.py createsuperuser

# Start the development server
python manage.py runserver

Step 6: Test the Views
Test 1: Public Endpoints
bash

# Test book list (should work without auth)
curl http://127.0.0.1:8000/api/books/list/

# Test book detail (should work without auth)
curl http://127.0.0.1:8000/api/books/1/

# Test search (should work without auth)
curl "http://127.0.0.1:8000/api/books/search/?search=harry"

Test 2: Protected Endpoints
bash

# Try to create book without auth (should fail)
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Book", "author": 1, "publication_year": 2024}'

# Create book with auth (replace with your credentials)
curl -X POST http://127.0.0.1:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -u yourusername:yourpassword \
  -d '{"title": "Test Book", "author": 1, "publication_year": 2024}'

Test 3: Admin Endpoints
bash

# Try to delete book as regular user (should fail)
curl -X DELETE http://127.0.0.1:8000/api/books/1/delete/ \
  -u regularuser:password

# Delete book as admin (should work)
curl -X DELETE http://127.0.0.1:8000/api/books/1/delete/ \
  -u adminuser:adminpassword




