from django.shortcuts import render
from rest_framework import viewsets, generics
from django.contrib.auth.models import User
from main.models import Event, Profile, Alumni, About, Project, Contact, Activity, CarouselImage, Linit, Timeline
from main import serializers
from main.forms import ProfileForm, ProfileChangeForm, MemberRegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.urls import reverse, NoReverseMatch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import datetime
import json


def register(request):
    if request.method == "POST":
        # form = UserCreationForm(request.POST)
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.save()
            return HttpResponseRedirect(reverse('admin:index'))
    else:
        form = MemberRegistrationForm
    args = {'form': form}
    return render(request, 'registration/register.html', args)


@login_required
def create_profile(request):
    if Profile.objects.filter(user=request.user).exists():
        messages.add_message(request, messages.INFO, 'A Profile already exists for user %s' % request.user.username)
        return HttpResponseRedirect(reverse('admin:index'))

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_form.save(user_id=request.user.pk)
            messages.add_message(request, messages.INFO,
                                 '%s, your Profile has been successfully created.' % request.user.username)
            return HttpResponseRedirect(reverse('admin:index'))
    else:
        profile_form = ProfileForm
        args = {'profile_form': profile_form}
        return render(request, 'profile/createprofile.html', args)


@login_required
def change_profile(request):
    if not Profile.objects.filter(user=request.user).exists():
        messages.add_message(request, messages.ERROR,
                             'No Profile Exists for %s, create one first.' % request.user.username)
        return HttpResponseRedirect(reverse('main:createprofile'))

    if request.method == "POST":
        profile_obj = Profile.objects.get(user=request.user)
        profile_form = ProfileChangeForm(request.POST, request.FILES, instance=profile_obj)
        if profile_form.is_valid():
            profile_form.save(user_id=request.user.pk)
            messages.add_message(request, messages.INFO,
                                 '%s, your Profile has been successfully updated.' % request.user.username)
            return HttpResponseRedirect(reverse('admin:index'))
    else:
        profile_obj = Profile.objects.get(user=request.user)
        profile_form = ProfileChangeForm(instance=profile_obj)
        args = {'profile_form': profile_form}
        return render(request, 'profile/changeprofile.html', args)


@staff_member_required
def convert_to_alumni(request):
    if datetime.datetime.today().month > 5:
        profiles = Profile.objects.filter(passout_year__lte=datetime.datetime.today().year)
    else:
        profiles = Profile.objects.filter(passout_year__lt=datetime.datetime.today().year)
    
    if request.method == "POST":
        ids = json.loads(request.POST.get("json_sent"))
        for idx in ids:
            profile = Profile.objects.get(id=idx)
            profile.convert_to_alumni = True
            profile.save(commit=True)
        return HttpResponseRedirect(reverse("main:convert2alumni"))
    return render(request, "profile/batch_convert_alumni.html", {"profiles": profiles})


class GetCount(APIView):
    """Return count for Members, Alumni,Events, and Projects"""
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        alumni = len(Alumni.objects.all())
        members = len(Profile.objects.all())
        events = len(Event.objects.all())
        projects = len(Project.objects.all())

        return Response({"members": members, "alumni": alumni,"events": events, "projects": projects})


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer
    lookup_field = 'identifier'
    http_method_names = ['get']


event_list = EventViewSet.as_view({'get': 'list'})

event_detail = EventViewSet.as_view({'get': 'retrieve'})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    http_method_names = ['get']


class AlumniViewSet(viewsets.ModelViewSet):
    queryset = Alumni.objects.all()
    serializer_class = serializers.AlumniSerializer
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


class CarouselImageViewSet(viewsets.ModelViewSet):
    queryset = CarouselImage.objects.all()
    serializer_class = serializers.CarouselImageSerializers
    http_method_names = ['get']


class LinitViewSet(viewsets.ModelViewSet):
    queryset = Linit.objects.all()
    serializer_class = serializers.LinitSerializers
    http_method_names = ['get']


class TimelineViewSet(viewsets.ModelViewSet):
    queryset = Timeline.objects.all().order_by('-id')
    serializer_class = serializers.TimelineSerializers
    http_method_names = ['get']
