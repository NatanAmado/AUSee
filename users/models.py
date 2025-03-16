from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

MAJOR_CHOICES = [
    ("Sciences", "Sciences"),
    ("Social Sciences", "Social Sciences"),
    ("Humanities", "Humanities"),
]


class CustomUser(AbstractUser):
    joined_date = models.DateTimeField(auto_now_add=True)
    major = models.CharField(max_length=50, choices=MAJOR_CHOICES, default='Sciences')
    track = models.CharField(max_length=80)
    email = models.EmailField(unique=False, default='\'@student.auc.nl\'', blank=False)
