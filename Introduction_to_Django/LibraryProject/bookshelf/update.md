# Update Operation

## Command:
```
book = Book.objects.get(title="1984") <--- Retrieves a book with the title "1984" in the database

book.title = "Nineteen Eighty-Four" <--- Updates book title to "Nineteen Eighty-Four".

book.save() <--- Saves changes to book title

book <--- Prints book with updated title