from django import forms
from django.forms import ModelForm
from main.models import Profile, SpecialToken
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

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
        # Add to a basic group when created
        if Group.objects.filter(name='BlogAuthors').exists():
            group = Group.objects.get(name='BlogAuthors')
            profile.user.groups.add(group)
        if commit:
            profile.user.save()
            profile.save()
        return profile

class ProfileChangeForm(ModelForm):
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
    def __init__(self, *args, **kwargs):
        super(ProfileChangeForm, self).__init__(*args, **kwargs)


    def save(self, user_id ,commit=True,):
        profile = super(ProfileChangeForm, self).save(commit=False)
        profile.user = User.objects.get(pk=user_id)
        if commit:
            profile.save()
        return profile


class MemberRegistrationForm(UserCreationForm):
    token = forms.CharField(label="Member Token", max_length=16)

    class Meta:
        model = User
        fields = ['token', 'username']

    def clean_token(self):
        token = self.cleaned_data['token']
        if SpecialToken.objects.filter(value=token).exists():
            _token = SpecialToken.objects.get(value=token)
            if _token.is_valid():
                _token.used += 1
                _token.save()
                return token
            else:
                raise forms.ValidationError("Token Expired")
        else:
            raise forms.ValidationError("Invalid Token")

    def save(self, commit=True):
        user = super(MemberRegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user
