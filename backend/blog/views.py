from rest_framework import generics
from .models import Author, Blog
from .serializers import AuthorSerializer, BlogSerializer

class AuthorListCreate(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BlogListCreate(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class AuthorReadAll(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BlogReadAll(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
