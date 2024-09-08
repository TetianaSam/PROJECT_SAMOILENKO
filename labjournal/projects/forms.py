from django import forms
from .models import Project, ProjectAccess
from django.contrib.auth.models import User

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'project_description', 'date_start', 'date_finish', 'file']  # Поле owner не включається у форму
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': False}),
            'date_start': forms.DateInput(attrs={'type': 'date'}),
            'date_finish': forms.DateInput(attrs={'type': 'date'}),
            'project_description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False  # Робимо поле файлу необов'язковим

class ProjectAccessForm(forms.ModelForm):
    class Meta:
        model = ProjectAccess
        fields = ['user', 'access_level']

    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if project:
            # Фільтрувати користувачів, щоб показати тільки тих, хто ще не має доступу
            self.fields['user'].queryset = User.objects.exclude(projectaccess__project=project)


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)
