
from django import forms
from .models import Notes, NoteAccess
from django.contrib.auth.models import User

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['owner', 'note_topic', 'note_text', 'file']  # Переконайтеся, що ім'я поля правильне
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False  # Робимо поле файлу необов'язковим

class NoteAccessForm(forms.ModelForm):
    class Meta:
        model = NoteAccess
        fields = ['user', 'access_level']

    def __init__(self, *args, **kwargs):
        note = kwargs.pop('note', None)
        super().__init__(*args, **kwargs)
        if note:
            # Фільтрувати користувачів, щоб показати тільки тих, хто ще не має доступу
            self.fields['user'].queryset = User.objects.exclude(noteaccess__note=note)

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)
