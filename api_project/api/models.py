from django.db import models
from django.conf import settings

# Create your models here.

class Book(models.Model):
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    isbn = models.CharField(max_length=13, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='books',
            null=True,
            blank=True

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"

def save(self, *args, **kwargs):

    if not self.created_by and hasattr(self, '_current_user'):
        self.created_by = self._current_user
    super().save(*args, **kwargs)