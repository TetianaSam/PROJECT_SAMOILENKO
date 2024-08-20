from django import forms
from .models import Resource, Suggestion

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['link', 'description', 'application_area']

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['link', 'description', 'application_area']
