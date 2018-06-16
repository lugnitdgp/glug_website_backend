from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User
from main.models import Event, Profile
from main.serializers import EventSerializer, ProfileSerializer, UserSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'identifier'

event_list = EventViewSet.as_view({
    'get':'list',
    'post':'create'
})

event_detail = EventViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer