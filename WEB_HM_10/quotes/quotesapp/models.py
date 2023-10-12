from django.db import models

# Create your models here.


class Author(models.Model):
    fullname = models.CharField(max_length=25, null=False, unique=True)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=25, null=False, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=25, null=False, unique=True)

class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

   




  
