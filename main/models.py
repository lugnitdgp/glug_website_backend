from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    identifier = models.CharField(max_length = 64, unique=True)
    title = models.CharField(max_length = 255)
    event_image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    
    #Choices of status
    STATUS = (
        ('DRAFT', 'Draft'),
        ('FINAL', 'Final'),
    )
    #Choices of event type
    TYPE =(
        ('ONLINE', 'Online'),
        ('WORKSHOP', 'Workshop'),
        ('TALK', 'Talk Show'),
        ('OFFLINE', 'Other Offline'),
    )

    event_type = models.CharField(max_length=64, choices=TYPE)
    venue = models.CharField(max_length=255, blank =True, null= True)
    event_timing = models.DateTimeField(blank =True, null= True)
    pub_date = models.DateTimeField(auto_now=True)
    pub_by = models.CharField(max_length=255, blank=True, null=True)
    edited_by = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=64, choices=STATUS)
    show = models.BooleanField(default = True)

    def __str__(self):
        return self.identifier


class Profile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    alias = models.CharField(max_length=64, blank=True, null=True)
    image = models.ImageField(upload_to='member_images/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)

    degree_name = models.CharField(max_length = 64)
    year_name = models.CharField(max_length = 16)

    def __str__(self):
        return self.first_name

class ImageCard(models.Model):
    image = models.ImageField()