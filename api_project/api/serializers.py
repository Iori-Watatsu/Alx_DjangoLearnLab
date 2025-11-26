from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):

    created_by = serializers.ReadOnlyField(source='created_by.username')
    created_by_email = serializers.ReadOnlyField(source='created_by.email')

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year', 'isbn', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

        def validate_publication_year(self, value):

            if value < 1000 or value > 2030:
            raise serializers.ValidationError("Publication year must be between 1000 and 2030.")
        return value

    def validate_title(self, value):

        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()

    def validate_author(self, value):

        if not value.strip():
            raise serializers.ValidationError("Author cannot be empty.")
        return value.strip()

    def create(self, validated_data):

        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)