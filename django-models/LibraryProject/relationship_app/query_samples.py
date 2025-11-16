import os
import sys
import django

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def run_queries():
    # -------------------------
    # Query all books by a specific author
    # -------------------------
    author_name = "John Doe"
    try:
        author = Author.objects.get(name=author_name)  
        books_by_author = Book.objects.filter(author=author)
        print(f"\nBooks by {author_name}:")
        for book in books_by_author:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")

    # -------------------------
    # List all books in a library
    # -------------------------
    library_name = "Central Library"
    try:
        library = Library.objects.get(name=library_name)
        books_in_library = library.books.all()
        print(f"\nBooks in {library_name}:")
        for book in books_in_library:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")

    # -------------------------
    # Retrieve the librarian for a library
    # -------------------------
    try:
        librarian = Librarian.objects.get(library=library)
        print(f"\nLibrarian for {library_name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to '{library_name}'.")


if __name__ == "__main__":
    run_queries()
    