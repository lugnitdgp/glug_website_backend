from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Post(models.Model):
    identifier = models.CharField(max_length=128, unique=True)
    featured = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    author_user = models.ForeignKey(User, on_delete=models.CASCADE)
    #Author's full name will be fatched from Profile model on main app
    author_name = models.CharField(max_length=255, blank=True, null=True,
    help_text="This will be shown in Blogs, If its not provided `username` of User will be used.")

    thumbnail_image = models.ImageField(upload_to='blog_tumbnails/', blank=True, null=True)
    content_body = RichTextField()

    pub_date = models.DateTimeField(auto_now_add=True)
    date_to_show = models.DateTimeField(blank=True, null=True)
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.identifier

    def save(self, *args, **kwargs):
        if not self.author_name:
            self.author_name = self.author_user.username
        if not self.date_to_show:
            self.date_to_show = self.pub_date
        
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent_id = models.SmallIntegerField(default=0)
    user_social_id = models.CharField(max_length=255, null=True, blank=True)
    user_social_name = models.CharField(max_length=255, null=True, blank=True)
    data = models.TextField(max_length=1024)
    
    def __str__(self):
        str_repr = self.data[:51]+"..." if (len(self.data) >= 52) else self.data
        return str_repr