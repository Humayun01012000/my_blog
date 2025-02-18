from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User


# 🏷️ Category Model

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_posts', kwargs={'category_id': self.pk})  # Use 'category_id'


# 📝 Post Model
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest posts first

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()

    def __str__(self):
        return f"{self.title} by {self.user.username}"


# 💬 Comment Model (Supports Replies)
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commented_posts')
    content = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Show latest comments first

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

    def user_avatar(self):
        return self.user.profile.profile_image.url if hasattr(self.user, 'profile') and self.user.profile.profile_image else '/media/default_profile.jpg'


# ❤️ Like Model
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')

    class Meta:
        unique_together = ('post', 'user')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"


# 🔖 Bookmark Model
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarked_posts')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='bookmarks')

    class Meta:
        unique_together = ('user', 'post')  # Prevent duplicate bookmarks

    def __str__(self):
        return f"{self.user.username} bookmarked {self.post.title}"

# 👤 User Profile Model (Now with Avatars)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='default_profile.jpg', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def avatar_url(self):
        return self.profile_image.url if self.profile_image else '/media/default_profile.jpg'
