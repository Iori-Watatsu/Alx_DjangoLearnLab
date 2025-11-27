from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Author, Book
from .serializers import BookSerializer, AuthorSerializer


class ModelTests(TestCase):
    """
Test model functionality, validation, and methods.
"""

    def setUp(self):
        """Set up test data for model tests."""
        self.author = Author.objects.create(name='Test Author')

    def test_author_creation(self):
        """Test author model creation and string representation."""
        author = Author.objects.create(name='J.R.R. Tolkien')
        self.assertEqual(str(author), 'J.R.R. Tolkien')
        self.assertEqual(author.name, 'J.R.R. Tolkien')

    def test_book_creation(self):
        """Test book model creation and string representation."""
        book = Book.objects.create(
            title='The Hobbit',
            author=self.author,
            publication_year=1937
        )
        self.assertEqual(str(book), '"The Hobbit" by Test Author')
        self.assertEqual(book.title, 'The Hobbit')
        self.assertEqual(book.author, self.author)

    def test_author_name_validation(self):
        """Test author name validation."""
        # Empty name should raise validation error
        author = Author(name='')
        with self.assertRaises(ValidationError):
            author.full_clean()

        # Whitespace-only name should be cleaned
        author = Author(name='  test author  ')
        author.full_clean()
        author.save()
        self.assertEqual(author.name, 'Test Author')

    def test_book_title_validation(self):
        """Test book title validation."""
        # Empty title should raise validation error
        book = Book(title='', author=self.author, publication_year=2024)
        with self.assertRaises(ValidationError):
            book.full_clean()

    def test_book_publication_year_validation(self):
        """Test book publication year validation."""
        current_year = timezone.now().year

        # Future year should raise validation error
        book = Book(title='Future Book', author=self.author, publication_year=current_year + 1)
        with self.assertRaises(ValidationError):
            book.full_clean()

        # Year before 1000 should raise validation error
        book = Book(title='Ancient Book', author=self.author, publication_year=999)
        with self.assertRaises(ValidationError):
            book.full_clean()

    def test_author_ordering(self):
        """Test that authors are ordered by name."""
        author1 = Author.objects.create(name='Z Author')
        author2 = Author.objects.create(name='A Author')

        authors = Author.objects.all()
        self.assertEqual(authors[0].name, 'A Author')
        self.assertEqual(authors[1].name, 'Test Author')
        self.assertEqual(authors[2].name, 'Z Author')

    def test_book_ordering(self):
        """Test that books are ordered by title."""
        book1 = Book.objects.create(title='Z Book', author=self.author, publication_year=2000)
        book2 = Book.objects.create(title='A Book', author=self.author, publication_year=2000)

        books = Book.objects.all()
        self.assertEqual(books[0].title, 'A Book')
        self.assertEqual(books[1].title, 'Z Book')


class SerializerTests(TestCase):
    """
Test serializer functionality and validation.
"""

    def setUp(self):
        """Set up test data for serializer tests."""
        self.author = Author.objects.create(name='Test Author')
        self.book_data = {
            'title': 'Test Book',
            'author': self.author.id,
            'publication_year': 2020,
            'isbn': '1234567890123'
        }

    def test_book_serializer_valid_data(self):
        """Test book serializer with valid data."""
        serializer = BookSerializer(data=self.book_data)
        self.assertTrue(serializer.is_valid())

    def test_book_serializer_invalid_data(self):
        """Test book serializer with invalid data."""
        # Empty title
        invalid_data = self.book_data.copy()
        invalid_data['title'] = ''
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

        # Future publication year
        invalid_data = self.book_data.copy()
        invalid_data['publication_year'] = timezone.now().year + 1
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)

    def test_book_serializer_output(self):
        """Test book serializer output structure."""
        book = Book.objects.create(
            title='Test Book',
            author=self.author,
            publication_year=2020
        )
        serializer = BookSerializer(book)

        expected_fields = ['id', 'title', 'author', 'publication_year', 'isbn', 'created_at', 'updated_at']
        for field in expected_fields:
            self.assertIn(field, serializer.data)

    def test_author_serializer_with_books(self):
        """Test author serializer with nested books."""
        book = Book.objects.create(
            title='Test Book',
            author=self.author,
            publication_year=2020
        )

        serializer = AuthorSerializer(self.author)

        self.assertIn('name', serializer.data)
        self.assertIn('books', serializer.data)
        self.assertEqual(len(serializer.data['books']), 1)
        self.assertEqual(serializer.data['books'][0]['title'], 'Test Book')