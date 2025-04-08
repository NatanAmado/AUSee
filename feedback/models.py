from django.db import models
from users.models import UNIVERSITY_COLLEGE_CHOICES

# Create your models here.


class Feedback(models.Model):
    name = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    university_college = models.CharField(max_length=4, choices=UNIVERSITY_COLLEGE_CHOICES, default='auc')

    def __str__(self):
        return f"Feedback from {self.name.username}"
    