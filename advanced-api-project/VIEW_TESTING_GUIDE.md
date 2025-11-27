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