from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='protocols_user_files')
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='user_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title



class Protocol(models.Model):
    name = models.CharField(max_length=100)
    protocol_text = models.TextField(default="N/A")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    projects = models.ManyToManyField(Project, related_name='protocols', blank=True)  # Додано
    file = models.FileField(upload_to='protocols/', blank=True, null=True)  # Робимо поле файлу необов'язковим

    def __str__(self):
        return self.name
