
from django import forms
from .models import Notes, NoteAccess, NoteFile
from django.forms import modelformset_factory
from django.contrib.auth.models import User
from projects.models import Project

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['note_topic', 'note_text', 'projects', 'protocols', 'reagents', 'consumables']
        widgets = {
            'projects': forms.CheckboxSelectMultiple,
            'protocols': forms.CheckboxSelectMultiple,
            'reagents': forms.CheckboxSelectMultiple,
            'consumables': forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Робимо всі ManyToMany поля необов'язковими
        self.fields['projects'].required = False
        self.fields['protocols'].required = False
        self.fields['reagents'].required = False
        self.fields['consumables'].required = False

NoteFileFormSet = modelformset_factory(NoteFile, fields=('file',), extra=5)

class NoteAccessForm(forms.ModelForm):
    class Meta:
        model = NoteAccess
        fields = ['user', 'access_level']

    def __init__(self, *args, **kwargs):
        note = kwargs.pop('note', None)
        super().__init__(*args, **kwargs)
        if note:
            # Фільтрувати користувачів, щоб показати тільки тих, хто ще не має доступу до цієї нотатки
            self.fields['user'].queryset = User.objects.exclude(noteaccess__note=note)
class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search')
    date_from = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    note_topic = forms.CharField(required=False, label='Note Topic')
    sort_by = forms.ChoiceField(
        choices=[('date_of_action', 'Date of Action'), ('created_at', 'Created At'), ('updated_at', 'Updated At')],
        required=False,
        initial='date_of_action'
    )