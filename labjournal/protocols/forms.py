from django import forms
from .models import Protocol,Project


class ProtocolForm(forms.ModelForm):
    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Можна використовувати інші виджети, якщо потрібно
        required=False
    )
    class Meta:
        model = Protocol
        fields = ['name', 'file', 'protocol_text','projects']  # Включіть інші поля моделі, якщо потрібно
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False  # Робимо поле файлу необов'язковим

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)