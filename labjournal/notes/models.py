from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from protocols.models import Protocol
from reagents.models import Reagents
from reagents.models import Consumables



class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes_user_files')
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='user_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class NoteFile(models.Model):
    note = models.ForeignKey('Notes', on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='notes/files/')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.note.note_topic} uploaded on {self.uploaded_at}"

class Notes(models.Model):
    READ = 'read'
    WRITE = 'write'
    ACCESS_CHOICES = [
        (READ, 'Read'),
        (WRITE, 'Write'),
    ]

    date_of_action = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_notes')
    note_topic = models.CharField(max_length=150)
    note_text = models.TextField()  # Changed to TextField for better handling of long text

    projects = models.ManyToManyField(Project, related_name='notes', blank=True)
    protocols = models.ManyToManyField(Protocol, related_name='notes', blank=True)
    reagents = models.ManyToManyField(Reagents, related_name='notes', blank=True)
    consumables = models.ManyToManyField(Consumables, related_name='notes', blank=True)

    access_level = models.CharField(max_length=10, choices=ACCESS_CHOICES, default=READ)

    def __str__(self):
        return self.note_topic

    class Meta:
        indexes = [
            models.Index(fields=['owner', 'note_topic']),
        ]


class NoteAccess(models.Model):
    READ = 'read'
    WRITE = 'write'
    ACCESS_CHOICES = [
        (READ, 'Read'),
        (WRITE, 'Write'),
    ]

    note = models.ForeignKey(Notes, on_delete=models.CASCADE, related_name='access_permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=10, choices=ACCESS_CHOICES, default=READ)

    class Meta:
        unique_together = ('note', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.note.note_topic} ({self.get_access_level_display()})'
