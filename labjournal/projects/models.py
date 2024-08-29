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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')  # Власник проекту
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_start = models.DateField()
    date_finish = models.DateField()
    file = models.FileField(upload_to='projects/', blank=True, null=True)  # Робимо поле файлу необов'язковим

    def __str__(self):
        return self.name

class ProjectAccess(models.Model):
    READ = 'read'
    WRITE = 'write'
    ACCESS_CHOICES = [
        (READ, 'Read'),
        (WRITE, 'Write'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='access_permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=10, choices=ACCESS_CHOICES, default=READ)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.project.name} ({self.get_access_level_display()})'