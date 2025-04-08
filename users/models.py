from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

MAJOR_CHOICES = [
    ("Sciences", "Sciences"),
    ("Social Sciences", "Social Sciences"),
    ("Humanities", "Humanities"),
]

UNIVERSITY_COLLEGE_CHOICES = [
    ('auc', 'Amsterdam University College'),
    ('luc', 'Leiden University College'),
    ('ucu', 'University College Utrecht'),
    ('ucr', 'University College Roosevelt'),
    ('ucm', 'University College Maastricht'),
    ('ucg', 'University College Groningen'),
    ('uct', 'University College Twente'),
    ('uctm', 'University College Tilburg Maastricht'),
]


class CustomUser(AbstractUser):
    joined_date = models.DateTimeField(auto_now_add=True)
    major = models.CharField(max_length=50, choices=MAJOR_CHOICES, default='Sciences')
    track = models.CharField(max_length=80)
    email = models.EmailField(unique=False, default='\'@student.auc.nl\'', blank=False)
    university_college = models.CharField(max_length=4, choices=UNIVERSITY_COLLEGE_CHOICES, default='auc')
