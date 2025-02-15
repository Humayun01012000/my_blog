from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User  # Import the User model 


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_posts', kwargs={'pk': self.pk})

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # Add ForeignKey to User
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Add category
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})  # Reverse URL for Post

    def __str__(self):
        return self.title
