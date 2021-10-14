from django import forms
from django.forms import ModelForm
from .models import Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['owner']
        widgets = {
            'tags': forms.CheckboxSelectMultiple
        }

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'review']
        labels = { 'value': 'Place your vote', 'review': 'Add a comment with your vote'}