from django.db import models

class Resource(models.Model):
    link = models.URLField(max_length=200)
    description = models.TextField()
    application_area = models.CharField(max_length=100)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

class Suggestion(models.Model):
    link = models.URLField(max_length=200)
    description = models.TextField()
    application_area = models.CharField(max_length=100)
    reviewed = models.BooleanField(default=False)
    suggested_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
from django.db import models

# Create your models here.
