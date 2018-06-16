from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Event, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff')

class EventSerializer(serializers.ModelSerializer):
    """Event fields serializer"""
    class Meta:
        model = Event
        fields = ('id','identifier','title','description','venue','status')


class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer"""
    class Meta:
        model = Profile
        fields = ('id', 'first_name','last_name','alias','degree_name','year_name')
