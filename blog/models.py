from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Post(models.Model):
    identifier = models.CharField(max_length=128, unique=True)
    featured = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    author_user = models.ForeignKey(User, on_delete=models.CASCADE)
    #Author's full name will be fatched from Profile model on main app
    author_alternate_name = models.CharField(max_length=255, blank=True, null=True)

    thumbnail_image = models.ImageField(upload_to='blog_tumbnails/', blank=True, null=True)
    content_body = RichTextField()

    pub_date = models.DateTimeField(auto_now_add=True)
    date_to_show = models.DateTimeField(blank=True, null=True)
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.identifier
