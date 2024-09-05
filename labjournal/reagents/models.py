from django.db import models
from django.contrib.auth.models import User

class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reagents_user_files')
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='user_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Reagents(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_reagents')
    name = models.CharField(max_length=100)
    units = models.CharField(max_length=100)
    amount =models.IntegerField(default=0)
    storage_temperature =models.CharField(max_length=100)
    cat_number =models.CharField(max_length=100)
    lot = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    reagent_description = models.TextField(default="N/A")
    delivery_date = models.DateField()
    expiration_date = models.DateField()

    file = models.FileField(upload_to='reagents/', blank=True, null=True)  # Робимо поле файлу необов'язковим

    #def __str__(self):
       #return self.name

class ReagentsAccess(models.Model):
    READ = 'read'
    WRITE = 'write'
    ACCESS_CHOICES = [
        (READ, 'Read'),
        (WRITE, 'Write'),
    ]

    reagent = models.ForeignKey(Reagents, on_delete=models.CASCADE, related_name='access_permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=10, choices=ACCESS_CHOICES, default=READ)

    class Meta:
        unique_together = ('reagent', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.reagent.name} ({self.get_access_level_display()})'

class Consumables(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_consumables')
    name = models.CharField(max_length=100)
    units = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    storage_temp = models.CharField(max_length=100)
    cat_number = models.CharField(max_length=100)
    lot = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    consumable_descr = models.TextField(default="N/A")
    delivery_date = models.DateField()
    expiration_date = models.DateField()

    file = models.FileField(upload_to='consumables/', blank=True, null=True)

    def __str__(self):
        return self.name

class ConsumablesAccess(models.Model):
    READ = 'read'
    WRITE = 'write'
    ACCESS_CHOICES = [
        (READ, 'Read'),
        (WRITE, 'Write'),
    ]

    consumable = models.ForeignKey(Consumables, on_delete=models.CASCADE, related_name='access_permissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=10, choices=ACCESS_CHOICES, default=READ)

    class Meta:
        unique_together = ('consumable', 'user')

    def __str__(self):
        return f'{self.user.username} - {self.consumable.name} ({self.get_access_level_display()})'
