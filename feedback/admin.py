from django.contrib import admin

# Register your models here.
# feedback/admin.py
from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'email', 'created_at')
    search_fields = ('feedback', 'email', 'created_at')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
