from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'project_description', 'date_start', 'date_finish', 'file']  # Поле owner не включається у форму
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False  # Робимо поле файлу необов'язковим


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)
