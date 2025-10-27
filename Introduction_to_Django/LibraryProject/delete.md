# Delete Operation

## Command:
```
book = Book.objects.get(title="Nineteen Eighty-Four") <--- Retrieves a book with the title "Nineteen Eighty-Four" in the database

book.delete() <--- Deletes book from Database

Book.objects.all() <--- Prints all books within the database