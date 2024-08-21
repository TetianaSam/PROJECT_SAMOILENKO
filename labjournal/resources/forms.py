from django import forms
from .models import Resource, Suggestion

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['link', 'description', 'application_area']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['link'].required = False  # Робимо поле файлу необов'язковим
class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ['link', 'description', 'application_area']
class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)