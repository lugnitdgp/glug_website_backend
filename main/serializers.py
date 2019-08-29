from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Event, Profile, About, Project, Contact, Activity, CarouselImage, Linit, Timeline
import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff')


class EventSerializer(serializers.ModelSerializer):
    """Event fields serializer"""
    show_bool = serializers.SerializerMethodField('check_show')

    def check_show(self, obj):
        if obj.show == False:
            obj.identifier = None
            obj.title = None
            obj.id = None
            obj.description = None
            obj.venue = None
            obj.url = None
            obj.event_timing = None
            obj.facebook_link = None
            obj.event_image = None
            obj.status = None
            return False

        elif obj.show == True:
            return True

    class Meta:
        model = Event
        fields = ('show_bool', 'id', 'identifier', 'title', 'description', 'venue',
                  'url', 'event_timing', 'facebook_link', 'event_image', 'status')


class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer"""
    # Using Metod field to get a field value of OnetoOneFiled
    user_name = serializers.SerializerMethodField('get_username')
    year_name = serializers.SerializerMethodField('get_year')

    def get_year(self, obj):
        # After Month May(5) a academic year changes
        if(datetime.date.today().month > 5):
            return (5-(obj.passout_year-datetime.date.today().year))
        else:
            return (5-(obj.passout_year-datetime.date.today().year)-1)

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Profile
        fields = ('id', 'user_name', 'first_name', 'last_name', 'alias', 'bio', 'year_name', 'position',
                  'email', 'image', 'degree_name', 'git_link', 'facebook_link', 'reddit_link', 'linkedin_link')


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ('identifier', 'heading', 'content')


class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('identifier', 'title', 'description', 'gitlink')


class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'phone_number', 'message')


class ActivitySerializers(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('title', 'description', 'image')


class CarouselImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = CarouselImage
        fields = ('identifier', 'image', 'heading', 'sub_heading')


class LinitSerializers(serializers.ModelSerializer):
    class Meta:
        model = Linit
        fields = ('title', 'description', 'image', 'year_edition', 'pdf')


class TimelineSerializers(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = '__all__'
