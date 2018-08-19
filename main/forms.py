from django import forms
from django.forms import ModelForm
from main.models import Profile
from django.contrib.auth.models import User

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'image',
            'bio',
            'email',
            'phone_number',
            'degree_name',
            'passout_year',
            'git_link',
            'facebook_link',
            'twitter_link',
            'linkedin_link',
            'reddit_link'
        ]
    
    def save(self, user_id ,commit=True,):
        profile = super(ProfileForm, self).save(commit=False)
        profile.user = User.objects.get(pk=user_id)
        if commit:
            profile.save()
        return profile
