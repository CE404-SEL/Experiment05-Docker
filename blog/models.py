from django.db import models


class Author(models.Model):
    full_name = models.CharField(max_length=255, null=False, blank=True)
    description = models.CharField(max_length=255, null=False, blank=True)
    age = models.PositiveIntegerField()
    github = models.URLField()
    linkedin = models.URLField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.full_name} - {self.description}"


class Blog(models.Model):
    author = models.ForeignKey(Author, related_name='blogs', on_delete=models.CASCADE)
    markdown = models.TextField()
    title = models.CharField(blank=False, null=False, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.author.full_name} - {self.title}"
