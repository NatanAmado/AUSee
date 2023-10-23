from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    joined_date = models.DateTimeField(auto_now_add=True)
