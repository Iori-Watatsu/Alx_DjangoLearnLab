# LibraryProject

## Overview
This is the initial setup for a Django-based web application named **LibraryProject**.
It serves as the foundation for developing Django applications, and helps you understand the framework’s default project structure.

---

## Step-by-Step Setup Instructions

Ensure Python is installed on your machine.

python --version

### 1. Create a virtual environment (recommended name: venv)

python -m venv venv

### 2. Activate the virtual environment:

Windows: venv\Scripts\activate

macOS / Linux: source venv/bin/activate

### 3. With the virtual environment active, install Django using pip:

pip install django

### 4. Verify the installation:

django-admin --version

### 5. Create your project using the django-admin command:

django-admin startproject LibraryProject

### 6. Understand the Project Structure

| File / Folder       | Description                                                                                                |
| ------------------- | ---------------------------------------------------------------------------------------------------------- |
| **manage.py**       | A command-line utility that lets you interact with your Django project (run the server, migrations, etc.). |
| **LibraryProject/** | The inner project directory containing all Django configuration files.                                     |
| **__init__.py**     | Marks this directory as a Python package.                                                                  |
| **settings.py**     | Stores configuration settings for the project (database, apps, middleware, etc.).                          |
| **urls.py**         | Defines URL routes for the project.                                                                        |
| **wsgi.py**         | Entry point for WSGI-compatible web servers.                                                               |
| **asgi.py**         | Entry point for ASGI-compatible asynchronous servers.                                                      |

### 7. Run the Development Server

cd LibraryProject
python manage.py runserver

You should see output similar to:

Starting development server at http://127.0.0.1:8000/

