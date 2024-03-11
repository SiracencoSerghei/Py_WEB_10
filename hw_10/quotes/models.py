from django.db import models

class Author(models.Model):
    fullname = models.CharField(max_length=120)
    # born_date = models.DateField()
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name = models.CharField(max_length=32,null = False, unique=True)
    
class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
