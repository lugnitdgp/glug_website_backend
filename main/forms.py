from django import forms
from django.forms import ModelForm
from main.models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'user',
            'image',
            'bio',
            'email',
            'phone_number',
            'degree_name',
            'year_name',
            'git_link',
            'facebook_link',
            'twitter_link',
            'linkedin_link',
            'reddit_link'
        ]
