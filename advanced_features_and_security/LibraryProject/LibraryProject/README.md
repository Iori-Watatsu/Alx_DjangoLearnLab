# Library Management System

A Django-based library management system with advanced user authentication, permissions, and groups management.

## Features

- **Custom User Model**: Email-based authentication instead of username
- **Book Management**: CRUD operations for books with permissions
- **Blog System**: Posts and comments with user interactions
- **Permission System**: Custom permissions and group-based access control
- **Object-level Permissions**: Users can only edit/delete their own content
- **Admin Interface**: Django admin integration for management

## Project Structure
LibraryProject/
├── bookshelf/ # Main application
│ ├── models.py # Custom User, Book, Post, Comment models
│ ├── views.py # Views with permission checks
│ ├── forms.py # Django forms for models
│ ├── urls.py # Application URL routing
│ ├── admin.py # Admin site configuration
│ └── management/commands/ # Custom management commands
├── LibraryProject/ # Project settings
│ ├── settings.py # Django settings
│ ├── urls.py # Project URL routing
│ └── wsgi.py # WSGI configuration
└── templates/ # HTML templates
└── bookshelf/ # App-specific templates


## Technology Stack

- **Backend**: Django 4.x
- **Database**: SQLite (default, can be configured for PostgreSQL/MySQL)
- **Authentication**: Custom user model with email
- **Frontend**: Bootstrap 5 for styling
- **Permissions**: Django's built-in permission system with custom groups

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LibraryProject
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py create_book_test_users

python manage.py runserver

Access the application

    Main site: http://localhost:8000/

    Admin interface: http://localhost:8000/admin/

Groups and Permissions
Pre-configured Groups

The system includes three main groups with specific permissions:
1. Book_Viewers

    Permissions: can_view

    Access: Can only view books

    Test User: viewer@library.com / testpass123

2. Book_Editors

    Permissions: can_view, can_create, can_edit

    Access: Can view, create, and edit books

    Test User: editor@library.com / testpass123

3. Book_Admins

    Permissions: can_view, can_create, can_edit, can_delete

    Access: Full access to all book operations

    Test User: admin@library.com / testpass123

Custom Permissions

The Book model includes these custom permissions:

    can_view - View books

    can_create - Create new books

    can_edit - Edit existing books

    can_delete - Delete books

Models
CustomUser

    Email as primary identifier (no username)

    Additional fields: date_of_birth, profile_photo

    Custom user manager for creating users and superusers

Book

    Basic book information: title, author, publication_year

    Ownership tracking: created_by, created_at, updated_at

    Availability status: is_available

Post

    Blog posts with title and content

    Author reference to CustomUser

    Timestamps for creation and updates

Comment

    Comments on posts

    Author reference to CustomUser

    Foreign key to Post

Views and Permissions

All views include permission checks using Django's permission system:
Book Views

    book_list - Requires can_view permission

    book_create - Requires can_create permission

    book_edit - Requires can_edit permission + object-level check

    book_delete - Requires can_delete permission + object-level check

Permission Enforcement Methods

    View-level permissions: Using @permission_required decorator

    Template-level permissions: Using {% if perms.app_name.permission_codename %}

    Object-level permissions: Custom methods in models

Management Commands
Setup Groups and Permissions
bash

python manage.py setup_book_permissions

Creates groups and assigns appropriate permissions.
Create Test Data
bash

python manage.py create_book_test_users

Creates test users and sample books for testing.
Testing the Permissions

    Log in as different users and test access levels

    Try to perform actions beyond user's permission level

    Verify error messages and access restrictions

    Check object-level permissions - users can only edit/delete their own content

Test User Credentials

    Viewer: viewer@library.com / testpass123

        Can only view books

    Editor: editor@library.com / testpass123

        Can view, create, and edit books

    Admin: admin@library.com / testpass123

        Full access to all operations

API Endpoints
Books

    GET /bookshelf/books/ - List all books

    GET /bookshelf/books/create/ - Create book form

    GET /bookshelf/books/<pk>/ - Book details

    GET /bookshelf/books/<pk>/edit/ - Edit book form

    POST /bookshelf/books/<pk>/delete/ - Delete book

Posts

    GET /bookshelf/posts/ - List all posts

    GET /bookshelf/posts/create/ - Create post form

    GET /bookshelf/posts/<pk>/edit/ - Edit post form

    POST /bookshelf/posts/<pk>/delete/ - Delete post

Comments

    GET /bookshelf/posts/<post_pk>/comment/ - Create comment

    GET /bookshelf/comments/<pk>/edit/ - Edit comment

    POST /bookshelf/comments/<pk>/delete/ - Delete comment

Customization
Adding New Permissions

    Add to model's Meta class:

python

class Meta:
    permissions = [
        ("custom_permission", "Custom permission description"),
    ]

    Run migrations:

bash

python manage.py makemigrations
python manage.py migrate

    Assign to groups in admin or via management commands

Adding New Groups

    Use Django admin interface, or

    Create management command, or

    Use Django shell:

bash

python manage.py shell

python

from django.contrib.auth.models import Group, Permission
group = Group.objects.create(name='NewGroup')
group.permissions.add(permission_object)

Deployment
Production Settings

    Set DEBUG = False

    Configure allowed hosts

    Set up proper database (PostgreSQL recommended)

    Configure static files serving

    Set up SSL certificate

    Use environment variables for sensitive data

Environment Variables

Create a .env file for production:
text

DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@host:port/database

Contributing

    Fork the repository

    Create a feature branch

    Make your changes

    Add tests for new functionality

    Submit a pull request

License

This project is licensed under the MIT License.
Support

For support and questions:

    Check the Django documentation

    Review the code comments

    Create an issue in the repository

Note: This project was developed as part of the ALX Django Learning Lab for educational purposes.
text