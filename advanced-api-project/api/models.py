from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class Author(models.Model):

    name = models.CharField(
        max_length=100,
        help_text="Full name of the author"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):

        return self.name

    def clean(self):

        if not self.name or not self.name.strip():
            raise ValidationError({'name': 'Author name cannot be empty.'})

        self.name = self.name.strip().title()

    def save(self, *args, **kwargs):

        self.full_clean()
        super().save(*args, **kwargs)


class Book(models.Model):

    title = models.CharField(
        max_length=200,
        help_text="Title of the book"
    )
    publication_year = models.IntegerField(
        help_text="Year the book was published"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="Author who wrote this book"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

        unique_together = ['title', 'author']

    def __str__(self):

        return f'"{self.title}" by {self.author.name}'

    def clean(self):

        current_year = timezone.now().year

        if not self.title or not self.title.strip():
            raise ValidationError({'title': 'Book title cannot be empty.'})

        if self.publication_year > current_year:
            raise ValidationError({
                'publication_year': f'Publication year cannot be in the future. Current year is {current_year}.'
            })

        if self.publication_year < 1000:
            raise ValidationError({
                'publication_year': 'Publication year must be after 1000 AD.'
            })

        self.title = self.title.strip()

    def save(self, *args, **kwargs):

        self.full_clean()
        super().save(*args, **kwargs)