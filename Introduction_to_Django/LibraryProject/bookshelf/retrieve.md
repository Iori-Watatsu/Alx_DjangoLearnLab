# Retrieve Operation

## Command:
```
from bookshelf.models import Book

book = Book.objects.get(title="1984") <--- Retrieves a book with the title "1984" in the database

book.title, book.author, book.publication_year <--- Prints the book