from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(default='default.png', upload_to='profile_images/', null=True, blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, **kwargs):
        super(Profile, self).save(**kwargs)

        img = Image.open(self.profile_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)
