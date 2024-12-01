from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    last_questionnaire = models.DateTimeField(null=True, blank=True)
    preferences = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

class Questionnaire(models.Model):
    CHOICES = [
        (1, 'Muito Mal'),
        (2, 'Mal'),
        (3, 'Normal'),
        (4, 'Bem'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    mood = models.IntegerField(choices=CHOICES)
    anxiety_level = models.IntegerField(choices=CHOICES)
    social_level = models.IntegerField(choices=CHOICES)
    energy_level = models.IntegerField(choices=CHOICES)
    stress_level = models.IntegerField(choices=CHOICES)
    sleep_quality = models.IntegerField(choices=CHOICES)
    appetite = models.IntegerField(choices=CHOICES)
    focus_level = models.IntegerField(choices=CHOICES)
    motivation = models.IntegerField(choices=CHOICES)
    suicidal_thoughts = models.IntegerField(choices=CHOICES)

    def __str__(self):
        return f'Questionário de {self.user.username} em {self.date}'

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    questionnaire = models.OneToOneField(Questionnaire, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    songs = models.JSONField()
    mood_category = models.CharField(max_length=50)

    def __str__(self):
        return f'Playlist de {self.user.username} - {self.created_at}'
