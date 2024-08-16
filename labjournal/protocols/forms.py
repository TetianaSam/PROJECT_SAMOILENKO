from django import forms
from .models import Protocol


class ProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = ['name', 'file', 'protocol_text']  # Включіть інші поля моделі, якщо потрібно
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False  # Робимо поле файлу необов'язковим
