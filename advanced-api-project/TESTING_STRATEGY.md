# Testing Strategy and Documentation

## Overview
This document outlines the comprehensive testing strategy for the Django REST Framework API project. The test suite ensures the integrity, security, and functionality of all API endpoints.

## Authentication Methods Tested

### 1. Token Authentication
- Uses `self.client.credentials()` with token headers
- Tests API key-based authentication
- Covers token creation and validation

### 2. Session Authentication
- Uses `self.client.login()` and `self.client.logout()`
- Tests Django's built-in session authentication
- Verifies login/logout functionality

## Test Structure

### Test Files
- `tests_views.py`: API endpoint tests (CRUD, filtering, authentication)
- `tests_models.py`: Model and serializer tests (validation, data integrity)

### Test Categories

#### 1. CRUD Operations
- **Create**: Test book/author creation with valid/invalid data
- **Read**: Test listing and retrieving individual resources
- **Update**: Test modifying existing resources
- **Delete**: Test resource deletion with proper permissions

#### 2. Filtering, Searching, and Ordering
- **Filtering**: Test field-based filtering, range filters, custom filters
- **Searching**: Test text search across multiple fields
- **Ordering**: Test ascending/descending ordering by various fields

#### 3. Authentication and Permissions
- **Token Authentication**: Test access with valid/invalid tokens
- **Session Authentication**: Test login/logout functionality
- **Permission Levels**: Test public, authenticated, and admin-only endpoints
- **Access Control**: Verify proper restriction of unauthorized access

#### 4. Error Handling
- **Invalid Input**: Test handling of malformed requests
- **Edge Cases**: Test boundary conditions and error scenarios
- **Nonexistent Resources**: Test 404 responses for invalid IDs

#### 5. Data Integrity
- **Response Structure**: Verify correct data structure and types
- **Validation**: Test model and serializer validation rules
- **Relationships**: Test foreign key relationships and nested serialization

## Running Tests

### Basic Test Execution
```bash
# Run all tests
python manage.py test api

# Run specific test file
python manage.py test api.tests_views
python manage.py test api.tests_models

# Run specific test class
python manage.py test api.tests_views.BookCRUDTests

# Run specific test method
python manage.py test api.tests_views.BookCRUDTests.test_create_book_authenticated

# Run with verbose output
python manage.py test api --verbosity=2

Test Database

    Tests use a separate SQLite in-memory database

    Test data is created in setUp methods and destroyed after each test

    No impact on development or production databases

Test Coverage

To measure test coverage (requires coverage package):
bash

pip install coverage
coverage run manage.py test api
coverage report
coverage html  # Generate HTML report

Authentication Testing
Session Authentication Tests

The test suite now includes comprehensive session authentication testing using self.client.login():
python

def test_session_authentication(self):
    # Test login functionality
    login_success = self.client.login(username='testuser', password='testpass123')
    self.assertTrue(login_success)

    # Test protected endpoint after login
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test logout functionality
    self.client.logout()
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

Token Authentication Tests

Also includes token authentication for API clients:
python

def test_token_authentication(self):
    # Set token in headers
    self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.regular_token.key}')

    # Test protected endpoint with token
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

Test Data Setup
Base Test Case (BaseAPITestCase)

    Creates regular user and admin user with authentication tokens

    Creates sample authors and books for testing

    Provides helper methods for both token and session authentication

Authentication Helper Methods

    authenticate_regular_user(): Token authentication for regular user

    authenticate_admin_user(): Token authentication for admin user

    login_regular_user(): Session authentication for regular user

    login_admin_user(): Session authentication for admin user

    remove_authentication(): Remove all authentication

Test Data Includes

    3 authors with different names

    5 books with varied publication years and authors

    Authentication tokens for different user roles

    User credentials for session authentication

Test Examples
Session Authentication Test
python

def test_create_book_authenticated_session(self):
    # Login using session authentication
    login_success = self.login_regular_user()
    self.assertTrue(login_success)

    # Perform authenticated action
    url = reverse('api:book-create')
    data = {'title': 'New Book', 'author': self.author1.id}
    response = self.client.post(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

Token Authentication Test
python

def test_create_book_authenticated_token(self):
    # Authenticate using token
    self.authenticate_regular_user()

    # Perform authenticated action
    url = reverse('api:book-create')
    data = {'title': 'New Book', 'author': self.author1.id}
    response = self.client.post(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

Authentication Failure Test
python

def test_create_book_unauthenticated(self):
    # Ensure no authentication
    self.remove_authentication()

    # Attempt protected action without auth
    url = reverse('api:book-create')
    data = {'title': 'New Book', 'author': self.author1.id}
    response = self.client.post(url, data, format='json')

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

Interpreting Test Results
Successful Tests

    All assertions pass

    Green output in test runner

    Exit code 0

Failed Tests

    One or more assertions fail

    Red output with failure details

    Exit code 1

Error Cases

    Exceptions during test execution

    Stack trace showing where error occurred

    Exit code 1

Common Test Outcomes

    OK: All tests passed

    FAILED: One or more tests failed

    ERROR: Unhandled exception in tests

Best Practices
Test Naming

    Use descriptive test method names

    Follow pattern: test_<scenario>_<expected_behavior>

    Group related tests in test classes

Test Isolation

    Each test should be independent

    Use setUp for common preparation

    Clean up after tests automatically

Authentication Testing

    Test both success and failure cases

    Verify different authentication methods

    Test permission levels thoroughly

Assertion Patterns

    Test one behavior per test method

    Use specific assertions for better error messages

    Verify both success and failure cases

Maintainability

    Keep tests focused and readable

    Use helper methods for complex setup

    Document test purpose with docstrings

Continuous Integration

These tests can be integrated into CI/CD pipelines to ensure code quality with every commit. The test suite runs quickly and provides comprehensive coverage of API functionality including both authentication methods.
text


## Step 3: Run the Updated Tests

Let's execute the updated test suite with session authentication:

```bash
# Make sure you're in the advanced-api-project directory
cd advanced-api-project

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Run all tests including the new session authentication tests
python manage.py test api --verbosity=2

# Run specific session authentication tests
python manage.py test api.tests_views.AuthenticationPermissionTests --verbosity=2

