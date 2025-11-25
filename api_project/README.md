# Django REST Framework API Project

This is a Django project set up with Django REST Framework for building APIs.


## Setup Instructions

1. **Navigate to the project directory:**
   ```bash
   cd api_project

2. # Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py runserver

API Endpoints

    Home: http://127.0.0.1:8000/

    API Root: http://127.0.0.1:8000/api/

    Books List/Create: http://127.0.0.1:8000/api/books/

    Book Detail: http://127.0.0.1:8000/api/books/{id}/

    Admin Panel: http://127.0.0.1:8000/admin/

Features

    Django REST Framework integration

    Book model with basic CRUD operations

    RESTful API endpoints

    Sample data loading command

    Admin interface for data management

Technologies Used

    Django 4.2+

    Django REST Framework

    SQLite database

    Python 3.8+

Now let's run the complete setup:

```bash
# Make sure you're in the api_project directory
cd api_project

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Load sample data
python manage.py load_sample_data

# Start the development server
python manage.py runserver

Verify the Setup

    Open your browser and go to http://127.0.0.1:8000/ - you should see the home page confirming the server is running.

    Visit http://127.0.0.1:8000/api/books/ to see the books API endpoint.

    Check http://127.0.0.1:8000/admin/ (you can create a superuser first with python manage.py createsuperuser if you want to access the admin).
