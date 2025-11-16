# Delete Operation

## Command:
```
from bookshelf.models import Book <--- Django loads the model and connects it to the database using the ORM (Object Relational Mapper)

book = Book.objects.get(title="Nineteen Eighty-Four") <--- Retrieves a book with the title "Nineteen Eighty-Four" in the database

book.delete() <--- Deletes book from Database

Book.objects.all() <--- Prints all books within the database