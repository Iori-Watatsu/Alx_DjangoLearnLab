from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"

from django.conf import settings

class Post(models.Model):
    """Example model that references the custom user model."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    """Another example model with user reference."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.email} on {self.post.title}"

class CustomUserManager(BaseUserManager):
    """Custom user manager for the CustomUser model."""

    def create_user(self, email, password=None, **extra_fields):
        """
Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model that uses email as the unique identifier."""

    # Remove the default username field and make email the unique identifier
    username = None
    email = models.EmailField(_('email address'), unique=True)

    # Additional custom fields
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    profile_photo = models.ImageField(
        _('profile photo'),
        upload_to='profile_photos/',
        null=True,
        blank=True
    )

    # Set the email field as the USERNAME_FIELD
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

class Post(models.Model):
    """Example model that references the custom user model."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Optional: Add permissions for Post model too
        permissions = [
            ("can_view_post", "Can view post"),
            ("can_create_post", "Can create post"),
            ("can_edit_post", "Can edit post"),
            ("can_delete_post", "Can delete post"),
        ]

    def __str__(self):
        return self.title

    # Object-level permission methods for Post
    def user_can_edit_post(self, user):
        return user == self.author or user.has_perm('bookshelf.can_edit_post')

    def user_can_delete_post(self, user):
        return user == self.author or user.has_perm('bookshelf.can_delete_post')


class Comment(models.Model):
    """Another example model with user reference."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Optional: Add permissions for Comment model
        permissions = [
            ("can_view_comment", "Can view comment"),
            ("can_create_comment", "Can create comment"),
            ("can_edit_comment", "Can edit comment"),
            ("can_delete_comment", "Can delete comment"),
        ]

    def __str__(self):
        return f"Comment by {self.author.email} on {self.post.title}"

    # Object-level permission methods for Comment
    def user_can_edit_comment(self, user):
        return user == self.author or user.has_perm('bookshelf.can_edit_comment')

    def user_can_delete_comment(self, user):
        return user == self.author or user.has_perm('bookshelf.can_delete_comment')


class CustomUserManager(BaseUserManager):
    """Custom user manager for the CustomUser model."""

    def create_user(self, email, password=None, **extra_fields):
        """
Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Custom user model that uses email as the unique identifier."""

    # Remove the default username field and make email the unique identifier
    username = None
    email = models.EmailField(_('email address'), unique=True)

    # Additional custom fields
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    profile_photo = models.ImageField(
        _('profile photo'),
        upload_to='profile_photos/',
        null=True,
        blank=True
    )

    # Set the email field as the USERNAME_FIELD
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')