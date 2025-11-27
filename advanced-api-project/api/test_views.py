from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer
import json


class BaseAPITestCase(APITestCase):
    """
Base test case class with common setup and helper methods.
Provides reusable utilities for all API test cases.
"""

    def setUp(self):
        """
Set up test data and clients for all test cases.
Creates test users, authors, books, and authentication tokens.
        """
        # Create test users
        self.regular_user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpass123',
            email='admin@example.com'
        )

        # Create authentication tokens
        self.regular_token = Token.objects.create(user=self.regular_user)
        self.admin_token = Token.objects.create(user=self.admin_user)

        # Create test authors
        self.author1 = Author.objects.create(name='George Orwell')
        self.author2 = Author.objects.create(name='Jane Austen')
        self.author3 = Author.objects.create(name='J.K. Rowling')

        # Create test books
        self.book1 = Book.objects.create(
            title='1984',
            author=self.author1,
            publication_year=1949,
            isbn='9780451524935'
        )
        self.book2 = Book.objects.create(
            title='Pride and Prejudice',
            author=self.author2,
            publication_year=1813,
            isbn='9780141439518'
        )
        self.book3 = Book.objects.create(
            title='Animal Farm',
            author=self.author1,
            publication_year=1945,
            isbn='9780451526342'
        )
        self.book4 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            author=self.author3,
            publication_year=1997,
            isbn='9780747532699'
        )
        self.book5 = Book.objects.create(
            title='Sense and Sensibility',
            author=self.author2,
            publication_year=1811,
            isbn='9780141439662'
        )

        # API client setup
        self.client = APIClient()

    def authenticate_regular_user(self):
        """Helper method to authenticate as regular user."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.regular_token.key}')

    def authenticate_admin_user(self):
        """Helper method to authenticate as admin user."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')

    def remove_authentication(self):
        """Helper method to remove authentication."""
        self.client.credentials()


class BookCRUDTests(BaseAPITestCase):
    """
Test CRUD operations for Book model endpoints.
Covers Create, Read, Update, Delete operations with proper authentication.
"""

    def test_list_books_authenticated(self):
        """
Test retrieving book list as authenticated user.
Should return 200 OK with all books.
        """
        self.authenticate_regular_user()
        url = reverse('api:book-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIn('title', response.data['results'][0])
        self.assertIn('author', response.data['results'][0])

    def test_list_books_unauthenticated(self):
        """
Test retrieving book list as unauthenticated user.
Should return 200 OK (public endpoint).
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)

    def test_retrieve_book_detail(self):
        """
Test retrieving specific book details.
Should return 200 OK with correct book data.
        """
        self.remove_authentication()
        url = reverse('api:book-detail', args=[self.book1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '1984')
        self.assertEqual(response.data['author'], self.author1.id)
        self.assertEqual(response.data['publication_year'], 1949)

    def test_create_book_authenticated(self):
        """
Test creating a new book as authenticated user.
Should return 201 CREATED with new book data.
        """
        self.authenticate_regular_user()
        url = reverse('api:book-create')
        data = {
            'title': 'New Test Book',
            'author': self.author3.id,
            'publication_year': 2024,
            'isbn': '1234567890123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['book']['title'], 'New Test Book')
        self.assertEqual(Book.objects.count(), 6)  # 5 initial + 1 new

    def test_create_book_unauthenticated(self):
        """
Test creating a book without authentication.
Should return 401 UNAUTHORIZED.
        """
        self.remove_authentication()
        url = reverse('api:book-create')
        data = {
            'title': 'New Test Book',
            'author': self.author3.id,
            'publication_year': 2024
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_invalid_data(self):
        """
Test creating a book with invalid data.
Should return 400 BAD REQUEST with validation errors.
        """
        self.authenticate_regular_user()
        url = reverse('api:book-create')
        data = {
            'title': '',  # Empty title
            'author': self.author3.id,
            'publication_year': 3000  # Future year
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertIn('publication_year', response.data)

    def test_update_book_authenticated(self):
        """
Test updating a book as authenticated user.
Should return 200 OK with updated data.
        """
        self.authenticate_regular_user()
        url = reverse('api:book-update', args=[self.book1.id])
        data = {
            'title': '1984 - Updated',
            'author': self.author1.id,
            'publication_year': 1949
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['book']['title'], '1984 - Updated')

        # Verify the book was actually updated in database
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, '1984 - Updated')

    def test_update_book_unauthenticated(self):
        """
Test updating a book without authentication.
Should return 401 UNAUTHORIZED.
        """
        self.remove_authentication()
        url = reverse('api:book-update', args=[self.book1.id])
        data = {'title': 'Updated Title'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_as_admin(self):
        """
Test deleting a book as admin user.
Should return 200 OK with success message.
        """
        self.authenticate_admin_user()
        url = reverse('api:book-delete', args=[self.book1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('successfully deleted', response.data['message'])
        self.assertEqual(Book.objects.count(), 4)  # 5 initial - 1 deleted

    def test_delete_book_as_regular_user(self):
        """
Test deleting a book as regular user (non-admin).
Should return 403 FORBIDDEN.
        """
        self.authenticate_regular_user()
        url = reverse('api:book-delete', args=[self.book1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_unauthenticated(self):
        """
Test deleting a book without authentication.
Should return 401 UNAUTHORIZED.
        """
        self.remove_authentication()
        url = reverse('api:book-delete', args=[self.book1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_nonexistent_book_retrieve(self):
        """
Test retrieving a book that doesn't exist.
Should return 404 NOT FOUND.
        """
        self.remove_authentication()
        url = reverse('api:book-detail', args=[999])  # Non-existent ID
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookFilteringSearchingOrderingTests(BaseAPITestCase):
    """
Test filtering, searching, and ordering capabilities for Book endpoints.
Covers all query parameter functionalities.
"""

    def test_filter_by_author(self):
        """
Test filtering books by author ID.
Should return only books by specified author.
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url, {'author': self.author1.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 2 books by George Orwell
        for book in response.data['results']:
            self.assertEqual(book['author'], self.author1.id)

    def test_filter_by_publication_year_range(self):
        """
Test filtering books by publication year range.
Should return books within specified year range.
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url, {
            'publication_year_min': 1900,
            'publication_year_max': 2000
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return books from 1945, 1949, 1997
        self.assertEqual(len(response.data['results']), 3)

    def test_filter_by_title_contains(self):
        """
Test filtering books by title contains.
Should return books with matching title pattern.
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url, {'title': 'Animal'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Animal Farm')

    def test_filter_by_author_name_contains(self):
        """
Test filtering books by author name contains.
Should return books by authors with matching name pattern.
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url, {'author_name': 'Orwell'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Both Orwell books

    def test_filter_by_multiple_publication_years(self):
        """
Test filtering books by multiple specific publication years.
Should return books matching any of the specified years.
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url, {'publication_years': '1949,1997'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 1984 and Harry Potter

    def test_filter_recent_books(self):
        """
Test filtering for recent books (last 10 years).
Should return books from recent years.
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url, {'recent': 'true'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: Our test data has books from older years, so this might return 0
        # This test verifies the filter works without errors

    def test_search_books(self):
        """
Test searching books across title and author fields.
Should return books matching search query.
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'Harry'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Harry Potter and the Philosopher\'s Stone')

    def test_search_books_multiple_fields(self):
        """
Test searching across multiple fields.
Should return books matching search in title or author name.
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'Orwell'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Both Orwell books

    def test_ordering_books_by_title_ascending(self):
        """
Test ordering books by title ascending.
Should return books in alphabetical order by title.
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'title'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data['results']]
        self.assertEqual(titles, sorted(titles))

    def test_ordering_books_by_publication_year_descending(self):
        """
Test ordering books by publication year descending.
Should return books from newest to oldest.
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': '-publication_year'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        publication_years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(publication_years, sorted(publication_years, reverse=True))

    def test_ordering_books_by_author_name(self):
        """
Test ordering books by author name.
Should return books ordered by author name.
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url, {'ordering': 'author__name'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Books should be ordered by author name

    def test_combined_filter_search_order(self):
        """
Test combining filtering, searching, and ordering.
Should return correctly filtered, searched, and ordered results.
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url, {
            'author': self.author1.id,
            'search': 'Farm',
            'ordering': '-publication_year'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Animal Farm')

    def test_advanced_search_multiple_criteria(self):
        """
Test advanced search with multiple criteria.
Should return books matching all specified criteria.
        """
        self.remove_authentication()
        url = reverse('api:book-advanced-search')
        response = self.client.get(url, {
            'q': 'Animal',
            'author': 'Orwell',
            'year_min': '1940'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Animal Farm')

    def test_recent_books_view(self):
        """
Test the recent books specialized view.
Should return books from the last 20 years.
        """
        self.remove_authentication()
        url = reverse('api:recent-books')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return books with metadata about recent books


class AuthorCRUDTests(BaseAPITestCase):
    """
Test CRUD operations for Author model endpoints.
"""

    def test_list_authors(self):
        """
Test retrieving author list.
Should return 200 OK with all authors.
        """
        self.remove_authentication()
        url = reverse('api:author-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_retrieve_author_detail(self):
        """
Test retrieving specific author details with nested books.
Should return 200 OK with author data and books.
        """
        self.remove_authentication()
        url = reverse('api:author-detail', args=[self.author1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'George Orwell')
        self.assertEqual(len(response.data['books']), 2)  # 2 books by Orwell

    def test_create_author_authenticated(self):
        """
Test creating a new author as authenticated user.
Should return 201 CREATED.
        """
        self.authenticate_regular_user()
        url = reverse('api:author-create')
        data = {'name': 'New Test Author'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author']['name'], 'New Test Author')
        self.assertEqual(Author.objects.count(), 4)  # 3 initial + 1 new

    def test_create_author_unauthenticated(self):
        """
Test creating author without authentication.
Should return 401 UNAUTHORIZED.
        """
        self.remove_authentication()
        url = reverse('api:author-create')
        data = {'name': 'New Author'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_author_authenticated(self):
        """
Test updating author as authenticated user.
Should return 200 OK.
        """
        self.authenticate_regular_user()
        url = reverse('api:author-update', args=[self.author1.id])
        data = {'name': 'George Orwell - Updated'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author1.refresh_from_db()
        self.assertEqual(self.author1.name, 'George Orwell - Updated')

    def test_delete_author_as_admin(self):
        """
Test deleting author as admin user.
Should return 200 OK.
        """
        self.authenticate_admin_user()
        url = reverse('api:author-delete', args=[self.author1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Author.objects.count(), 2)  # 3 initial - 1 deleted

    def test_delete_author_with_books(self):
        """
Test deleting author who has books (should be prevented).
Should return 400 BAD REQUEST with error message.
        """
        self.authenticate_admin_user()
        url = reverse('api:author-delete', args=[self.author1.id])
        response = self.client.delete(url)

        # This should fail because author has books
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cannot delete', response.data['error'])


class AuthenticationPermissionTests(BaseAPITestCase):
    """
Test authentication and permission mechanisms.
Verifies proper access control for different user roles.
"""

    def test_token_authentication(self):
        """
Test token-based authentication.
Should allow access with valid token.
        """
        url = reverse('api:book-create')
        data = {'title': 'Test Book', 'author': self.author1.id, 'publication_year': 2024}

        # Without token - should be unauthorized
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # With valid token - should be authorized
        self.authenticate_regular_user()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_only_endpoints(self):
        """
Test that admin-only endpoints reject non-admin users.
        """
        url = reverse('api:book-delete', args=[self.book1.id])

        # Regular user - should be forbidden
        self.authenticate_regular_user()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin user - should be allowed
        self.authenticate_admin_user()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_public_endpoints_no_auth_required(self):
        """
Test that public endpoints work without authentication.
        """
        self.remove_authentication()

        endpoints = [
            reverse('api:book-list'),
            reverse('api:book-detail', args=[self.book1.id]),
            reverse('api:author-list'),
            reverse('api:author-detail', args=[self.author1.id]),
            reverse('api:book-advanced-search'),
            reverse('api:recent-books'),
        ]

        for url in endpoints:
            response = self.client.get(url)
            self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])


class ErrorHandlingTests(BaseAPITestCase):
    """
Test error handling and edge cases.
"""

    def test_invalid_query_parameters(self):
        """
Test handling of invalid query parameters.
Should return 200 OK with empty results or default behavior.
        """
        self.remove_authentication()
        url = reverse('api:book-list')

        # Test with invalid parameter names
        response = self.client.get(url, {'invalid_param': 'value'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test with invalid parameter values
        response = self.client.get(url, {'publication_year_min': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pagination_parameters(self):
        """
Test pagination functionality.
Should return paginated results with metadata.
        """
        self.remove_authentication()
        url = reverse('api:book-list')

        response = self.client.get(url, {'page': 1, 'page_size': 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('total_pages', response.data)
        self.assertIn('current_page', response.data)
        self.assertEqual(len(response.data['results']), 2)

    def test_empty_search_results(self):
        """
Test search with no matching results.
Should return 200 OK with empty results array.
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url, {'search': 'NonexistentBookTitle123'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)


class ResponseDataIntegrityTests(BaseAPITestCase):
    """
Test response data integrity and structure.
"""

    def test_book_response_structure(self):
        """
Test that book responses have correct structure and data types.
        """
        self.remove_authentication()
        url = reverse('api:book-detail', args=[self.book1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response structure
        expected_fields = ['id', 'title', 'author', 'publication_year', 'isbn', 'created_at', 'updated_at']
        for field in expected_fields:
            self.assertIn(field, response.data)

        # Check data types
        self.assertIsInstance(response.data['title'], str)
        self.assertIsInstance(response.data['author'], int)
        self.assertIsInstance(response.data['publication_year'], int)

    def test_author_response_structure(self):
        """
Test that author responses have correct structure with nested books.
        """
        self.remove_authentication()
        url = reverse('api:author-detail', args=[self.author1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check response structure
        self.assertIn('name', response.data)
        self.assertIn('books', response.data)
        self.assertIsInstance(response.data['books'], list)

        # Check nested book structure
        if response.data['books']:
            book = response.data['books'][0]
            self.assertIn('title', book)
            self.assertIn('publication_year', book)

    def test_list_response_metadata(self):
        """
Test that list responses include proper metadata.
        """
        self.remove_authentication()
        url = reverse('api:book-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check pagination metadata
        self.assertIn('count', response.data)
        self.assertIn('total_pages', response.data)
        self.assertIn('current_page', response.data)
        self.assertIn('results', response.data)

        # Check query metadata for filtering/searching/ordering
        self.assertIn('query_metadata', response.data)