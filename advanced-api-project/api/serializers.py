# api/serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
   
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'publication_year',
            'author',
            'author_name',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author_name']

    def validate_publication_year(self, value):

        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )

        if value < 1000:
            raise serializers.ValidationError(
                "Publication year must be after 1000 AD."
            )

        return value

    def validate_title(self, value):

        if not value or not value.strip():
            raise serializers.ValidationError("Book title cannot be empty.")

        return value.strip()

    def create(self, validated_data):

        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.publication_year = validated_data.get('publication_year', instance.publication_year)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance


class AuthorSerializer(serializers.ModelSerializer):

    books = BookSerializer(many=True, read_only=True)
    book_count = serializers.IntegerField(source='books.count', read_only=True)

    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'book_count',
            'books',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'book_count']

    def validate_name(self, value):

        if not value or not value.strip():
            raise serializers.ValidationError("Author name cannot be empty.")

        return value.strip().title()

    def create(self, validated_data):

        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class AuthorSummarySerializer(serializers.ModelSerializer):

    book_count = serializers.IntegerField(source='books.count', read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'book_count', 'created_at']
        read_only_fields = ['id', 'book_count', 'created_at']