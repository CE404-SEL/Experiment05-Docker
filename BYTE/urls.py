from django.contrib import admin
from django.urls import path
from blog import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('authors/', blog_views.AuthorListCreate.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', blog_views.AuthorDetail.as_view(), name='author-detail'),
    path('authors/readall/', blog_views.AuthorReadAll.as_view(), name='author-readall'),

    path('blogs/', blog_views.BlogListCreate.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>/', blog_views.BlogDetail.as_view(), name='blog-detail'),
    path('blogs/readall/', blog_views.BlogReadAll.as_view(), name='blog-readall'),
]
