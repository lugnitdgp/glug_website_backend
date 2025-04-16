from calendar import month_name
from datetime import date
from django.shortcuts import render
from rest_framework import viewsets, generics
from django.contrib.auth.models import User
from main.models import Config, Event, Profile, CTF,Facad, Alumni, About, Project, Contact, Activity, CarouselImage, Linit, Timeline, LinitImage, TechBytes, DevPost
from main import serializers
from main.forms import ProfileForm, ProfileChangeForm, MemberRegistrationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from collections import defaultdict


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


class GetCount(APIView):
    """Return count for Members, Alumni,Events, and Projects"""
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        alumni = len(Alumni.objects.all())
        members = len(Profile.objects.all())
        events = len(Event.objects.all())
        projects = len(Project.objects.all())

        return Response({"members": members, "alumni": alumni, "events": events, "projects": projects})


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-event_timing')
    serializer_class = serializers.EventSerializer
    lookup_field = 'identifier'
    http_method_names = ['get']


event_list = EventViewSet.as_view({'get': 'list'})

event_detail = EventViewSet.as_view({'get': 'retrieve'})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    http_method_names = ['get']

class FacadViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows faculty advisors to be viewed or edited.
    """
    queryset = Facad.objects.all()
    serializer_class = serializers.FacadSerializer
    http_method_names = ['get']

class AlumniViewSet(viewsets.ModelViewSet):
    queryset = Alumni.objects.all().order_by('-passout_year', 'first_name')
    serializer_class = serializers.AlumniSerializer
    http_method_names = ['get']


# ViewSets define the view behavior.
class AlumniByYearViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AlumniSerializer
    http_method_names = ['get']
    #  We use the get_queryset() method instead of assigning a fixed queryset attribute 
    # such that the queryset is updated dynamically each time the view is accessed.
    def get_queryset(self):
        queryset = Alumni.objects.all().order_by('-passout_year', 'first_name')
        return queryset

    def list(self, request, *args, **kwargs):
        data = defaultdict(list)
        queryset = self.get_queryset()
        for alumni in queryset:
            data[alumni.passout_year].append(self.serializer_class(alumni).data)
        return Response(data)

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
    """
    API endpoint for Linit magazine entries
    """
    queryset = Linit.objects.all().order_by('-year_edition')
    serializer_class = serializers.LinitSerializer
    permission_classes = [AllowAny]


class LinitPages(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        year = request.GET['year']
        linit = Linit.objects.get(year_edition=int(year))
        linit_images = LinitImage.objects.filter(linit_year=linit)
        links = []
        for image in linit_images:
            links.append(request.build_absolute_uri(image.image.url))
        return Response({'links': links})


class TimelineViewSet(viewsets.ModelViewSet):
    queryset = Timeline.objects.all().order_by('-event_time')
    serializer_class = serializers.TimelineSerializers
    http_method_names = ['get']

class MonthlyTimelineViewSet(viewsets.ModelViewSet):
    queryset = Timeline.objects.all()
    serializer_class = serializers.TimelineSerializers
    http_method_names = ['get']
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-event_time')
    
    def group_by_month_year(self, queryset):
        current_year= date.today().year
        
        result = {f"{month} {year}": [] for year in range(current_year, current_year-3, -1) for month in month_name[1:]}
        for obj in queryset:
            
                month_year = obj.event_time.strftime("%B %Y")
                result.setdefault(month_year, []).append(serializers.TimelineSerializers(obj).data)
        return result

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        grouped_by_month_year = self.group_by_month_year(queryset)
        return Response(grouped_by_month_year)

class UpcomingEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().filter(upcoming=True)
    serializer_class = serializers.EventSerializer
    http_method_names = ['get']


class TechBytesViewSet(viewsets.ModelViewSet):
    queryset = TechBytes.objects.all()
    serializer_class = serializers.TechBytesSerializers
    http_method_names = ['get']

class DevPostViewSet(viewsets.ModelViewSet):
    queryset = DevPost.objects.all()
    serializer_class = serializers.DevPostSerializers
    http_method_names = ['get']


class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = serializers.ConfigSerializers
    http_method_names = ['get']

class CTFViewSet(viewsets.ModelViewSet):
    queryset = CTF.objects.all().order_by('-created_at')
    serializer_class = serializers.CTFSerializer
    http_method_names = ['get']  # Read-only API

    def get_serializer_context(self):
        return {'request': self.request}