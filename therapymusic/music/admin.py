from django.contrib import admin
from .models import UserProfile, Questionnaire, Playlist

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'last_questionnaire']
    search_fields = ['user__username']

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'mood', 'anxiety_level']
    list_filter = ['date', 'mood', 'anxiety_level']
    search_fields = ['user__username']

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'mood_category']
    list_filter = ['created_at', 'mood_category']
    search_fields = ['user__username']
    