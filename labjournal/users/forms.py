from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ['name', 'profile_image']

    def save(self, *args, **kwargs):
        profile = super(ProfileForm, self).save(*args, **kwargs)
        if self.cleaned_data['email']:
            profile.user.email = self.cleaned_data['email']
            profile.user.save()
        return profile
