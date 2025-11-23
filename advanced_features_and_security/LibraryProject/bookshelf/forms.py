"""
Forms for the bookshelf application with security best practices.

This module defines Django forms that include:
- Input validation and sanitization
- CSRF protection
- Secure file upload handling
- Custom validation methods
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import escape
import re
from .models import Book, Post, Comment, CustomUser

class BookForm(forms.ModelForm):
    """
Secure form for creating and updating Book instances.
Includes validation to prevent XSS and SQL injection attacks.
"""

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'is_available']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'maxlength': '200'  # Security: Enforce max length
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'maxlength': '100'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Publication year',
                'min': '1000',  # Security: Reasonable year range
                'max': '2030'
            }),
            'is_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'is_available': 'Available for borrowing'
        }
        help_texts = {
            'publication_year': 'Enter a valid year between 1000 and 2030.',
            'title': 'Book title should not contain special characters or scripts.'
        }

    def clean_title(self):
        """
Security: Custom validation for book title to prevent XSS and injection attacks.
        """
        title = self.cleaned_data.get('title', '').strip()

        if not title:
            raise ValidationError("Book title is required.")

        # Security: Check for potential XSS patterns
        xss_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'onload=',
            r'onerror=',
            r'onclick=',
            r'vbscript:',
        ]

        for pattern in xss_patterns:
            if re.search(pattern, title, re.IGNORECASE):
                raise ValidationError("Invalid characters detected in title.")

        # Security: Check for SQL injection patterns
        sql_patterns = [
            r'(\bUNION\b|\bSELECT\b|\bINSERT\b|\bDELETE\b|\bUPDATE\b|\bDROP\b|\bEXEC\b)',
            r'(\-\-|\#|\/\*|\*)',
            r'(\bOR\b|\bAND\b)\s+\d+=\d+',
            r'(\bWAITFOR\b|\bDELAY\b)',
        ]

        for pattern in sql_patterns:
            if re.search(pattern, title, re.IGNORECASE):
                raise ValidationError("Invalid input pattern detected.")

        # Security: Escape any HTML content to prevent XSS
        safe_title = escape(title)

        return safe_title

    def clean_author(self):
        """
Security: Custom validation for author field.
        """
        author = self.cleaned_data.get('author', '').strip()

        if not author:
            raise ValidationError("Author name is required.")

        # Security: Validate author name format (letters, spaces, hyphens, apostrophes)
        if not re.match(r'^[A-Za-z\s\-\'\.]+$', author):
            raise ValidationError("Author name contains invalid characters.")

        # Security: Escape any special characters
        safe_author = escape(author)

        return safe_author

    def clean_publication_year(self):
        """
Security: Validate publication year to be reasonable.
        """
        year = self.cleaned_data.get('publication_year')

        if year is None:
            raise ValidationError("Publication year is required.")

        # Security: Validate year range
        if year < 1000 or year > 2030:
            raise ValidationError("Please enter a valid publication year.")

        return year


class PostForm(forms.ModelForm):
    """
Secure form for creating and updating Post instances.
Includes content sanitization and validation.
"""

    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title',
                'maxlength': '200'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Enter post content',
                'maxlength': '5000'  # Security: Limit content length
            }),
        }
        help_texts = {
            'content': 'Maximum 5000 characters. Avoid using script tags or special code.'
        }

    def clean_title(self):
        """
Security: Validate post title for security.
        """
        title = self.cleaned_data.get('title', '').strip()

        if not title:
            raise ValidationError("Post title is required.")

        # Security: Check for XSS patterns
        if re.search(r'<script.*?>.*?</script>', title, re.IGNORECASE):
            raise ValidationError("Invalid characters in title.")

        safe_title = escape(title)
        return safe_title

    def clean_content(self):
        """
Security: Sanitize post content while allowing basic HTML formatting.
        """
        content = self.cleaned_data.get('content', '').strip()

        if not content:
            raise ValidationError("Post content is required.")

        # Security: Remove potentially dangerous tags but allow safe ones
        dangerous_tags = ['script', 'iframe', 'object', 'embed', 'form', 'input', 'button']

        for tag in dangerous_tags:
            # Remove opening tags
            content = re.sub(f'<{tag}.*?>', '', content, flags=re.IGNORECASE)
            # Remove closing tags
            content = re.sub(f'</{tag}>', '', content, flags=re.IGNORECASE)

        # Security: Remove event handlers
        event_handlers = ['onload', 'onerror', 'onclick', 'onmouseover', 'onkeypress']
        for handler in event_handlers:
            content = re.sub(f'{handler}=["\'].*?["\']', '', content, flags=re.IGNORECASE)

        # Security: Escape any remaining HTML that might be dangerous
        safe_content = escape(content)

        return safe_content


class CommentForm(forms.ModelForm):
    """
Secure form for creating and updating Comment instances.
"""

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your comment',
                'maxlength': '1000'
            }),
        }
        help_texts = {
            'content': 'Maximum 1000 characters. Be respectful in your comments.'
        }

    def clean_content(self):
        """
Security: Sanitize comment content.
        """
        content = self.cleaned_data.get('content', '').strip()

        if not content:
            raise ValidationError("Comment content is required.")

        if len(content) < 2:
            raise ValidationError("Comment is too short.")

        # Security: Remove any script tags
        content = re.sub(r'<script.*?>.*?</script>', '', content, flags=re.IGNORECASE)

        # Security: Escape HTML to prevent XSS
        safe_content = escape(content)

        return safe_content


class UserRegistrationForm(forms.ModelForm):
    """
Secure user registration form with password validation.
"""

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'minlength': '8'
        }),
        help_text='Password must be at least 8 characters long.'
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'date_of_birth']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your first name',
                'maxlength': '30'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your last name',
                'maxlength': '30'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

    def clean_email(self):
        """
Security: Validate and normalize email address.
        """
        email = self.cleaned_data.get('email', '').lower().strip()

        if not email:
            raise ValidationError("Email address is required.")

        # Security: Basic email format validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("Please enter a valid email address.")

        # Security: Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")

        return email

    def clean_first_name(self):
        """Security: Validate first name."""
        first_name = self.cleaned_data.get('first_name', '').strip()

        if not first_name:
            raise ValidationError("First name is required.")

        # Security: Only allow letters, spaces, hyphens, and apostrophes
        if not re.match(r'^[A-Za-z\s\-\'\.]+$', first_name):
            raise ValidationError("First name contains invalid characters.")

        safe_first_name = escape(first_name)
        return safe_first_name

    def clean_last_name(self):
        """Security: Validate last name."""
        last_name = self.cleaned_data.get('last_name', '').strip()

        if not last_name:
            raise ValidationError("Last name is required.")

        # Security: Only allow letters, spaces, hyphens, and apostrophes
        if not re.match(r'^[A-Za-z\s\-\'\.]+$', last_name):
            raise ValidationError("Last name contains invalid characters.")

        safe_last_name = escape(last_name)
        return safe_last_name

    def clean_password1(self):
        """Security: Validate password strength."""
        password1 = self.cleaned_data.get('password1', '')

        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        # Security: Check for common weak patterns
        if password1.lower() in ['password', '12345678', 'qwertyui']:
            raise ValidationError("This password is too common. Please choose a stronger one.")

        # Security: Check for at least one number and one letter
        if not re.search(r'[0-9]', password1) or not re.search(r'[a-zA-Z]', password1):
            raise ValidationError("Password must contain both letters and numbers.")

        return password1

    def clean(self):
        """
Security: Cross-field validation for password confirmation.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError({
                'password2': "Passwords do not match."
            })

        return cleaned_data

    def save(self, commit=True):
        """
Security: Create user with properly hashed password.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


class UserProfileForm(forms.ModelForm):
    """
Secure form for updating user profile information.
"""

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'date_of_birth', 'profile_photo']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '30'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '30'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'profile_photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean_first_name(self):
        """Security: Validate first name."""
        first_name = self.cleaned_data.get('first_name', '').strip()

        if first_name and not re.match(r'^[A-Za-z\s\-\'\.]+$', first_name):
            raise ValidationError("First name contains invalid characters.")

        return escape(first_name) if first_name else first_name

    def clean_last_name(self):
        """Security: Validate last name."""
        last_name = self.cleaned_data.get('last_name', '').strip()

        if last_name and not re.match(r'^[A-Za-z\s\-\'\.]+$', last_name):
            raise ValidationError("Last name contains invalid characters.")

        return escape(last_name) if last_name else last_name

    def clean_profile_photo(self):
        """
Security: Validate profile photo upload.
        """
        photo = self.cleaned_data.get('profile_photo')

        if photo:
            # Security: Validate file size (max 2MB)
            if photo.size > 2 * 1024 * 1024:
                raise ValidationError("Image file too large (maximum 2MB).")

            # Security: Validate file type
            valid_content_types = ['image/jpeg', 'image/png', 'image/gif']
            if photo.content_type not in valid_content_types:
                raise ValidationError("Unsupported file format. Please upload JPEG, PNG, or GIF.")

            # Security: Validate file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            import os
            ext = os.path.splitext(photo.name)[1].lower()
            if ext not in valid_extensions:
                raise ValidationError("Unsupported file extension.")

        return photo


class SearchForm(forms.Form):
    """
Secure search form with input validation to prevent injection attacks.
"""

    query = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books...',
            'maxlength': '100'
        }),
        help_text='Enter book title or author name to search.'
    )

    search_type = forms.ChoiceField(
        choices=[
            ('title', 'Title'),
            ('author', 'Author'),
            ('both', 'Both')
        ],
        initial='both',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    def clean_query(self):
        """
Security: Sanitize search query to prevent XSS and injection attacks.
        """
        query = self.cleaned_data.get('query', '').strip()

        if not query:
            raise ValidationError("Search query is required.")

        # Security: Remove potentially dangerous characters and patterns
        dangerous_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'vbscript:',
            r'onload=',
            r'onerror=',
            r'(\bUNION\b|\bSELECT\b|\bINSERT\b|\bDELETE\b|\bUPDATE\b|\bDROP\b|\bEXEC\b)',
            r'(\-\-|\#|\/\*|\*)',
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                raise ValidationError("Invalid search query.")

        # Security: Limit query length and escape special characters
        if len(query) > 100:
            raise ValidationError("Search query is too long.")

        safe_query = escape(query)
        return safe_query


class ContactForm(forms.Form):
    """
Secure contact form with comprehensive input validation.
"""

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name',
            'maxlength': '100'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email address'
        })
    )

    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject',
            'maxlength': '200'
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Your message',
            'maxlength': '2000'
        })
    )

    def clean_name(self):
        """Security: Validate name field."""
        name = self.cleaned_data.get('name', '').strip()

        if not name:
            raise ValidationError("Name is required.")

        if not re.match(r'^[A-Za-z\s\-\'\.]+$', name):
            raise ValidationError("Name contains invalid characters.")

        return escape(name)

    def clean_subject(self):
        """Security: Validate subject field."""
        subject = self.cleaned_data.get('subject', '').strip()

        if not subject:
            raise ValidationError("Subject is required.")

        # Check for XSS patterns
        if re.search(r'<script.*?>.*?</script>', subject, re.IGNORECASE):
            raise ValidationError("Invalid characters in subject.")

        return escape(subject)

    def clean_message(self):
        """Security: Sanitize message content."""
        message = self.cleaned_data.get('message', '').strip()

        if not message:
            raise ValidationError("Message is required.")

        # Remove dangerous tags but allow basic formatting
        dangerous_tags = ['script', 'iframe', 'object', 'embed']

        for tag in dangerous_tags:
            message = re.sub(f'<{tag}.*?>', '', message, flags=re.IGNORECASE)
            message = re.sub(f'</{tag}>', '', message, flags=re.IGNORECASE)

        safe_message = escape(message)
        return safe_message