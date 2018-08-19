from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Event, Profile, About, Project, Contact, Activity, ImageCard


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff')

class EventSerializer(serializers.ModelSerializer):
    """Event fields serializer"""
    show_bool = serializers.SerializerMethodField('check_show')

    def check_show(self,obj):     
        if obj.show == False:
            obj.identifier = None
            obj.title = None
            obj.id = None
            obj.description = None
            obj.venue = None
            obj.url = None
            obj.event_timing = None
            obj.event_image = None
            obj.status = None
            return False

        elif obj.show == True:
            return True
       
    class Meta:
        model = Event
        fields = ('show_bool', 'id','identifier','title','description','venue','url','event_timing','event_image','status')

class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer"""
    # Using Metod field to get a field value of OnetoOneFiled
    user_name = serializers.SerializerMethodField('get_username')
    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Profile
        fields = ('id', 'user_name','first_name','last_name','alias','position', 'email', 'image','degree_name','year_name','git_link', 'facebook_link', 'reddit_link','linkedin_link')


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ('identifier', 'heading', 'content')

class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('identifier','title','description','gitlink')

class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id','name','email','phone_number','message')

class ActivitySerializers(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('title','description','image')

class ImageCardSerializers(serializers.ModelSerializer):
    class Meta:
        model = ImageCard
        fields = ('card_id','image','cards_text')