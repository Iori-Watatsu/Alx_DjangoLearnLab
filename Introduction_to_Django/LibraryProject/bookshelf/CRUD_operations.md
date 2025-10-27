# CRUD Operations for the Book Model

This document contains all CRUD (Create, Retrieve, Update, Delete) operations performed on the `Book` model in the `bookshelf` app using Django’s ORM.
All commands are intended to be run in the Django shell (`python manage.py shell`).

---

## CRUD Operation

from bookshelf.models import Book

# Create a new book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
book

Expected Output:
<Book: 1984 by George Orwell (1949)>
# A new Book instance was successfully created and saved to the database.

# Retrieve the book by title
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year

Expected Output:
('1984', 'George Orwell', 1949)
# Successfully retrieved the book and displayed all its attributes.

# Update the book title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()  # Important: parentheses are required to save the change

# Verify the update
book

Expected Output:
<Book: Nineteen Eighty-Four by George Orwell (1949)>
# The book title was successfully updated in the database.

# Delete the book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Verify deletion
Book.objects.all()

Expected Output:
(1, {'bookshelf.Book': 1})
<QuerySet []>
# The book instance was successfully deleted. No books remain in the database.

