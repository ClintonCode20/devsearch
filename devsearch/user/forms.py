from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message
class CreateUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        exclude = ['owner']

class MessageUserForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']