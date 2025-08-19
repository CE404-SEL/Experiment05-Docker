from rest_framework import serializers
from .models import Author, Blog

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'full_name', 'age', 'description', 'github', 'linkedin', 'email']

class BlogSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Blog
        fields = ['id', 'author', 'markdown', 'title', 'created_at', 'is_active']
