from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Config, Event,CTF, Sponsor,Profile, Facad, Alumni, About, Project, Contact, Activity, CarouselImage, Linit, Timeline, TechBytes, DevPost
import datetime
import markdown


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff')


class EventSerializer(serializers.ModelSerializer):
    """Event fields serializer"""
    show_bool = serializers.SerializerMethodField('check_show')
    description_markdown = serializers.SerializerMethodField()
    bts_image_url = serializers.SerializerMethodField()
    bts_video_url = serializers.SerializerMethodField()

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
            obj.featured = None
            obj.upcoming = None
            obj.bts_description = None
            obj.bts_image = None
            obj.bts_video = None
            obj.bts_uploaded_at = None
            return False
        elif obj.show == True:
            return True

    def get_description_markdown(self, obj):
        if obj.description:
            return markdown.markdown(obj.description)
        return None

    def get_bts_image_url(self, obj):
        if obj.bts_image and obj.show:  # Only show if event is visible
            return self.context['request'].build_absolute_uri(obj.bts_image.url)
        return None

    def get_bts_video_url(self, obj):
        if obj.bts_video and obj.show:  # Only show if event is visible
            return self.context['request'].build_absolute_uri(obj.bts_video.url)
        return None

    class Meta:
        model = Event
        fields = (
            'show_bool', 'id', 'identifier', 'title', 'description', 'description_markdown', 
            'venue', 'url', 'event_timing', 'facebook_link', 'event_image', 'status', 
            'featured', 'upcoming', 'bts_description', 'bts_image', 'bts_image_url', 
            'bts_video', 'bts_video_url', 'bts_uploaded_at'
        )

class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer"""
    # Using Metod field to get a field value of OnetoOneFiled
    user_name = serializers.SerializerMethodField('get_username')
    year_name = serializers.SerializerMethodField('get_year')

    def get_year(self, obj):
        # After Month May(5) a academic year changes
        if (datetime.date.today().month > 5):
            return (5 - (obj.passout_year - datetime.date.today().year))
        else:
            return (5 - (obj.passout_year - datetime.date.today().year) - 1)

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Profile
        fields = ('id', 'user_name', 'first_name', 'last_name', 'alias', 'bio', 'year_name', 'position', 'email',
                  'image', 'degree_name', 'git_link', 'facebook_link', 'reddit_link', 'linkedin_link')

class FacadSerializer(serializers.ModelSerializer):
    """Faculty Advisor serializer"""
    class Meta:
        model = Facad
        fields = ('id', 'post', 'first_name', 'last_name', 'linkedin_link', 'email', 'image')

class AlumniSerializer(serializers.ModelSerializer):
    """Alumni Profile serializer"""
    class Meta:
        model = Alumni
        fields = ('id', 'first_name', 'last_name', 'alias', 'bio', 'passout_year', 'position', 'email',
                  'image', 'degree_name', 'git_link', 'facebook_link', 'twitter_link', 'reddit_link', 'linkedin_link')


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ('identifier', 'heading', 'content')


class ProjectSerializers(serializers.ModelSerializer):
    description_markdown = serializers.SerializerMethodField()

    def get_description_markdown(self, obj):
        if obj.description:
            return markdown.markdown(obj.description)
        return None

    class Meta:
        model = Project
        fields = ('id', 'identifier', 'title', 'description', 'description_markdown', 'gitlink')


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
        fields = ('identifier', 'image', 'mobile_image', 'heading', 'sub_heading')


class LinitSerializers(serializers.ModelSerializer):
    class Meta:
        model = Linit
        fields = ('title', 'description', 'image', 'year_edition')


class TimelineSerializers(serializers.ModelSerializer):
    detail_markdown = serializers.SerializerMethodField()
    class Meta:
        model = Timeline
        fields = ('id', 'event_name', 'detail', 'detail_markdown', 'event_time')

    def get_detail_markdown(self, obj):
        if obj.detail:
            return markdown.markdown(obj.detail)
        return None


class TechBytesSerializers(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

    class Meta:
        model = TechBytes
        fields = ('id', 'title', 'image', 'image_url', 'body', 'link', 'pub_date')


class DevPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = DevPost
        fields = '__all__'


class ConfigSerializers(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ('key', 'value', 'enable')


class SponsorSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    def get_logo_url(self, obj):
        if obj.logo:
            return self.context['request'].build_absolute_uri(obj.logo.url)
        return None

    class Meta:
        model = Sponsor  # This will now work
        fields = ('id', 'name', 'logo', 'logo_url', 'website')


class CTFSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    def get_photo_url(self, obj):
        if obj.photo:
            return self.context['request'].build_absolute_uri(obj.photo.url)
        return None

    class Meta:
        model = CTF
        fields = ('id', 'name', 'photo', 'photo_url', 'link', 'description', 'created_at')