from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.utils import timezone
import datetime
from django.forms.models import model_to_dict


def validate_pdf_size(value):
    limit = 100 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 100 MiB.')


def validate_image_size(value):
    limit = 1 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MiB.')


# Create your models here.


class Event(models.Model):
    identifier = models.CharField(max_length=64, unique=True, help_text="Unique Identifier for events")
    title = models.CharField(max_length=255)
    event_image = models.ImageField(upload_to='event_images/', null=True, blank=True, validators=[validate_image_size])
    description = RichTextField(blank=True, null=True)

    # Choices of status
    STATUS = (
        ('DRAFT', 'Draft'),
        ('FINAL', 'Final'),
    )
    # Choices of event type
    TYPE = (
        ('ONLINE', 'Online'),
        ('WORKSHOP', 'Workshop'),
        ('TALK', 'Talk Show'),
        ('OFFLINE', 'Other Offline'),
    )

    event_type = models.CharField(max_length=64, choices=TYPE)
    venue = models.CharField(max_length=255, blank=True, null=True, help_text="Venue for Offline Events.")
    url = models.URLField(max_length=255, blank=True, null=True, help_text="URL for Online Events.")
    event_timing = models.DateTimeField(blank=True, null=True)
    facebook_link = models.URLField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now=True)
    pub_by = models.CharField(max_length=255, blank=True, null=True)
    edited_by = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=64, choices=STATUS)
    show = models.BooleanField(default=True)
    add_to_timeline = models.BooleanField(default=False, help_text="To add to timeline.")
    featured = models.BooleanField(default=False)
    upcoming = models.BooleanField(default=True)

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

        if (self.add_to_timeline == True):
            if not Timeline.objects.filter(event_name=self.title).exists():
                Timeline.objects.create(event_name=self.title, detail=self.description)


def year_choices():
    cuur_year = datetime.date.today().year
    return [(y, y) for y in range(cuur_year, cuur_year + 4 + 1)]


class Profile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Choices of degree
    DEGREE = (
        ('BTECH', 'B.Tech'),
        ('MCA', 'MCA'),
        ('MTECH', 'M.Tech'),
    )

    YEAR = (
        ('1', 'First'),
        ('2', 'Second'),
        ('3', 'Third'),
        ('4', 'Final'),
    )

    alias = models.CharField(max_length=64, blank=True, null=True)
    bio = models.TextField(max_length=512, blank=True, null=True)
    image = models.ImageField(upload_to='member_images/', blank=True, null=True, validators=[validate_image_size])
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    degree_name = models.CharField(max_length=64, choices=DEGREE)
    passout_year = models.IntegerField(choices=year_choices(), default=2018)
    position = models.CharField(max_length=255, blank=True, null=True)
    convert_to_alumni = models.BooleanField(default=False)

    git_link = models.URLField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    reddit_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.first_name
    
    def save(self, *args, **kwargs):
        """
        Checks if the profile belongs to an alumni or not and converts to alumni if True
        """
        if self.convert_to_alumni == True:
            initial_data = model_to_dict(self)
            if self.user is not None:
                user = self.user
                user.is_active = False
            initial_data.pop('convert_to_alumni', None)
            initial_data.pop('user', None)
            alumni = Alumni(**initial_data)
            alumni.save()
            self.delete()
            return
        else: 
            super(Profile, self).save(*args, **kwargs)


class Alumni(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    # Choices of degree
    DEGREE = (
        ('BTECH', 'B.Tech'),
        ('MCA', 'MCA'),
        ('MTECH', 'M.Tech'),
    )

    alias = models.CharField(max_length=64, blank=True, null=True)
    bio = models.TextField(max_length=512, blank=True, null=True)
    image = models.ImageField(upload_to='alumni_images/', blank=True, null=True, validators=[validate_image_size])
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    degree_name = models.CharField(max_length=64, choices=DEGREE)
    passout_year = models.IntegerField(default=2018)
    position = models.CharField(max_length=255, blank=True, null=True)

    git_link = models.URLField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    reddit_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return (self.first_name + " " + self.last_name)


class CarouselImage(models.Model):
    identifier = models.CharField(max_length=64, unique=True)
    image = models.ImageField(upload_to='card_images/', validators=[validate_image_size])
    mobile_image = models.ImageField(upload_to='card_images/mobile/',
                                     validators=[validate_image_size],
                                     blank=True,
                                     null=True)
    heading = models.CharField(max_length=255, blank=True, null=True)
    sub_heading = models.TextField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.identifier


class About(models.Model):
    identifier = models.CharField(max_length=64, unique=True)
    # remove blank and null after test
    heading = models.CharField(max_length=255, blank=True, null=True)
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
    image = models.ImageField(upload_to='activity_images/', blank=True, null=True, validators=[validate_image_size])

    class Meta:
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.title


class Linit(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1024, blank=True, null=True)
    image = models.ImageField(upload_to='linit_images/', blank=True, null=True)
    year_edition = models.IntegerField(default=2018)
    pdf = models.FileField(upload_to='linit_pdfs/', blank=True, null=True, validators=[validate_pdf_size])
    pdf_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title


class SpecialToken(models.Model):
    """This is intended for special use cases,
        where a feature needs to be an
        'members only' feature"""

    name = models.CharField(max_length=255)
    value = models.CharField(max_length=16)
    used = models.SmallIntegerField(default=0)
    max_usage = models.IntegerField(default=1)
    valid_till = models.DateTimeField()

    def is_valid(self):
        t_now = timezone.now()
        if self.used < self.max_usage and t_now < self.valid_till:
            return True
        return False

    def set_valid_default(self):
        return datetime.datetime.now() + datetime.timedelta(hours=6)

    def save(self, *args, **kwargs):
        if not self.value:
            self.value = get_random_string(16)
        return super(SpecialToken, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Timeline(models.Model):
    event_name = models.CharField(max_length=120)
    detail = RichTextField()
    event_time = models.DateField(blank=True)

    def __str__(self):
        return self.event_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.event_time = timezone.now()
        return super(Timeline, self).save(*args, **kwargs)
