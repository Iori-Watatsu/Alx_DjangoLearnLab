#  Create Operation

## Command:
```
from bookshelf.models import Book <--- Django loads the model and connects it to the database using the ORM (Object Relational Mapper).

python manage.py shell <--- Starts Django Shell

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949) <--- Creates and stores Book

book <--- Shows book in database

