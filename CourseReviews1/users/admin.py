from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'joined_date', 'major', 'track']
    list_filter = ('major',)  # Allow filtering by major
    search_fields = ('username', 'email', 'major', 'track')  # Allow searching by these fields