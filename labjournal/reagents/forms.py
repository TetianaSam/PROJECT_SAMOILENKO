from django import forms
from .models import Reagents, ReagentsAccess, Consumables, ConsumablesAccess
from django.contrib.auth.models import User

class ReagentsForm(forms.ModelForm):
    class Meta:
        model = Reagents
        fields = ['name', 'units', 'amount','storage_temperature', 'cat_number', 'lot', 'producer','reagent_description',
                  'delivery_date', 'expiration_date', 'file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': False}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
            'reagent_description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False

class ReagentsAccessForm(forms.ModelForm):
    class Meta:
        model = ReagentsAccess
        fields = ['user', 'access_level']

    def __init__(self, *args, **kwargs):
        reagent = kwargs.pop('reagent', None)
        super().__init__(*args, **kwargs)
        if reagent:
            self.fields['user'].queryset = User.objects.exclude(reagentaccess__reagent=reagent)

class ConsumablesForm(forms.ModelForm):
    class Meta:
        model = Consumables
        fields = [
            'name',
            'units',
            'amount',
            'storage_temp',
            'cat_number',
            'lot',
            'producer',
            'consumable_descr',
            'delivery_date',
            'expiration_date',
            'file'
        ]
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
            'consumable_descr': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False

class ConsumablesAccessForm(forms.ModelForm):
    class Meta:
        model = ConsumablesAccess
        fields = ['user', 'access_level']

    def __init__(self, *args, **kwargs):
        consumable = kwargs.pop('consumable', None)
        super().__init__(*args, **kwargs)
        if consumable:
            self.fields['user'].queryset = User.objects.exclude(consumableaccess__consumable=consumable)

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)
