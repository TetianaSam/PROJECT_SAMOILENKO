from django.db import models
from django.contrib.auth.models import User

class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_user_files')
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='user_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Project(models.Model):
    name = models.CharField(max_length=100)
    project_description = models.TextField(default="N/A")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Власник проекту
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_start = models.DateField()
    date_finish = models.DateField()
    file = models.FileField(upload_to='projects/', blank=True, null=True)  # Робимо поле файлу необов'язковим

    def __str__(self):
        return self.name
