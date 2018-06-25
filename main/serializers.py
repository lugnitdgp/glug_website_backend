from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Event, Profile, About, Project, Contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff')

class EventSerializer(serializers.ModelSerializer):
    """Event fields serializer"""
    class Meta:
        model = Event
        fields = ('id','identifier','title','description','venue','url','event_timing','event_image','status')


class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer"""
    # Using Metod field to get a field value of OnetoOneFiled
    user_name = serializers.SerializerMethodField('get_username')
    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Profile
        fields = ('id', 'user_name','first_name','last_name','alias', 'email', 'image','degree_name','year_name','git_link', 'facebook_link', 'reddit_link')


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ('identifier', 'content')

class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('identifier','title','description','gitlink')

class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id','name','email','phone_number','message')    