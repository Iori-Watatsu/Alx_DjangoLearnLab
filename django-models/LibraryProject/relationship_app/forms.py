from django import forms
from .models import Book   # or whatever model you use

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        