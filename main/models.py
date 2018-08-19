from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import datetime

# Create your models here.
class Event(models.Model):
    identifier = models.CharField(max_length = 64, unique=True, help_text="Unique Identifier for events")
    title = models.CharField(max_length = 255)
    event_image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    description = RichTextField(blank=True, null=True)
    
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
    venue = models.CharField(max_length=255, blank=True, null=True, help_text="Venue for Offline Events.")
    url = models.URLField(max_length=255, blank=True, null=True, help_text="URL for Online Events.")
    event_timing = models.DateTimeField(blank =True, null= True)
    pub_date = models.DateTimeField(auto_now=True)
    pub_by = models.CharField(max_length=255, blank=True, null=True)
    edited_by = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=64, choices=STATUS)
    show = models.BooleanField(default = True)

    def __str__(self):
        return self.identifier
    
    def save(self, *args, **kwargs):
        # Check if Set to 'DRAFT' then set show to false
        # Check online/offline and set url or venue accordingly
        # Offline events may have links for other purpose
        if self.status == "DRAFT":
            self.show = False
        
        if self.event_type == "ONLINE":
            self.venue = None
        super().save(*args, **kwargs)


def year_choices():
    cuur_year = datetime.date.today().year
    return [(y,y) for y in range(cuur_year,cuur_year+4+1)]

class Profile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #Choices of degree
    DEGREE = (
        ('BTECH','B.Tech'),
        ('MCA','MCA'),
        ('MTECH','M.Tech'),
    )

    YEAR = (
        ('1','First'),
        ('2','Second'),
        ('3','Third'),
        ('4','Final'),
    )

    alias = models.CharField(max_length=64, blank=True, null=True)
    bio = models.TextField(max_length=512, blank=True, null=True)
    image = models.ImageField(upload_to='member_images/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    degree_name = models.CharField(max_length = 64, choices=DEGREE)
    # year_name = models.CharField(max_length = 16, choices=YEAR)
    passout_year = models.IntegerField(choices=year_choices(),default= 2018)
    position = models.CharField(max_length=255, blank=True, null=True)

    git_link = models.URLField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    reddit_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)


    def __str__(self):
        return self.first_name

class ImageCard(models.Model):
    card_id = models.CharField(max_length=64, unique=True)
    image = models.ImageField(upload_to='card_images/')
    cards_text = models.TextField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.card_id


class About(models.Model):
    identifier = models.CharField(max_length=64, unique=True)
    heading = models.CharField(max_length=255, blank=True, null=True) #remove blank and null after test
    content = RichTextField()

    def __str__(self):
        return self.identifier


class Project(models.Model):
    identifier = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=512)
    description = RichTextField()
    gitlink = models.URLField(null=True, blank=True)

class Contact(models.Model):
    """For Contact Us endpoint only"""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    message = models.TextField(max_length=1024, blank=True, null=True)

class Activity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1024, blank=True, null=True)
    image = models.ImageField(upload_to='activity_images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.title