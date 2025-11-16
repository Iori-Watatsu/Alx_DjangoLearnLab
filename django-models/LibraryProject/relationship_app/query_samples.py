import django
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# Setup Django environment if running as standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def run_queries():
    # Create sample data if it doesn't exist
    author, _ = Author.objects.get_or_create(name="John Doe")
    library, _ = Library.objects.get_or_create(name="Central Library")
    book1, _ = Book.objects.get_or_create(title="Python 101", author=author)
    book2, _ = Book.objects.get_or_create(title="Django Deep Dive", author=author)
    library.books.add(book1, book2)
    Librarian.objects.get_or_create(name="Alice", library=library)

    # Now queries
    books_by_author = Book.objects.filter(author=author)
    print(f"\nBooks by {author.name}:")
    for book in books_by_author:
        print(f"- {book.title}")

    books_in_library = library.books.all()
    print(f"\nBooks in {library.name}:")
    for book in books_in_library:
        print(f"- {book.title}")

    librarian = library.librarian
    print(f"\nLibrarian for {library.name}: {librarian.name}")    

if __name__ == "__main__":
    run_queries()
