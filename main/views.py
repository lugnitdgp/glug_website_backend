from django.shortcuts import render
from rest_framework import viewsets, generics
from django.contrib.auth.models import User
from main.models import Event, Profile, About, Project, Contact, Activity, ImageCard
from main import serializers
from main.forms import ProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return HttpResponseRedirect('/admin')
    else:
        form = UserCreationForm
        profile_form = ProfileForm
        args = {'form':form,'profile_form':profile_form}
        return render(request, 'registration/register.html', args)

@login_required
def create_profile(request):
    if Profile.objects.filter(user=request.user).exists():
        messages.add_message(request, messages.INFO, 'A Profile already exists for user %s' % request.user.username)
        return HttpResponseRedirect('/admin')

    if request.method == "POST":
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile_form.save(user_id=request.user.pk)
            return HttpResponseRedirect('/admin')
    else:
        profile_form = ProfileForm
        args = {'profile_form':profile_form}
        return render(request, 'profile/createprofile.html', args)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer
    lookup_field = 'identifier'
    http_method_names = ['get']

event_list = EventViewSet.as_view({
    'get':'list'
})

event_detail = EventViewSet.as_view({
    'get': 'retrieve'
})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    http_method_names = ['get']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'

class AboutViewSet(viewsets.ModelViewSet):
    queryset = About.objects.all()
    serializer_class = serializers.AboutSerializer
    lookup_field = 'identifier'
    http_method_names = ['get']

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializers
    lookup_field = 'identifier'
    http_method_names = ['get']

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = serializers.ContactSerializers
    http_method_names = ['get']

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = serializers.ActivitySerializers
    http_method_names = ['get']

class ImageCardViewSet(viewsets.ModelViewSet):
    queryset = ImageCard.objects.all()
    serializer_class = serializers.ImageCardSerializers
    http_method_names = ['get']