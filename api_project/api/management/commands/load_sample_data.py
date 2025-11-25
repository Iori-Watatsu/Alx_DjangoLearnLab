# api/management/commands/load_sample_data.py
from django.core.management.base import BaseCommand
from api.models import Book

class Command(BaseCommand):
    help = 'Load sample book data for API testing'

    def handle(self, *args, **options):
        sample_books = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'publication_year': 1925,
                'isbn': '9780743273565'
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'publication_year': 1960,
                'isbn': '9780061120084'
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'publication_year': 1949,
                'isbn': '9780451524935'
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'publication_year': 1813,
                'isbn': '9780141439518'
            },
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'publication_year': 1937,
                'isbn': '9780547928227'
            }
        ]

        books_created = 0
        for book_data in sample_books:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            if created:
                books_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {book.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {books_created} books')
        )