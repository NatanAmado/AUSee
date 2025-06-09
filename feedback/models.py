from django.db import models
from users.models import UNIVERSITY_COLLEGE_CHOICES

# Create your models here.


class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    feedback = models.TextField()
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anonymous Feedback - {self.created_at}"
    