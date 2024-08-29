from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.exceptions import ValidationError

class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 100  # Встановіть максимальну довжину за необхідності
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if value and len(value.split()) < 2:
            raise ValidationError('Name must contain at least a first and last name.')

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return value.strip().title() if value else value

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = NameField(blank=False)
    email = models.EmailField(max_length=254, unique=True, blank=True, null=True)  # Поле для email
    profile_image = models.ImageField(default='default.png', upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)


