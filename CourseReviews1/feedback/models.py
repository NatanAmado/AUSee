from django.db import models

# Create your models here.


class Feedback(models.Model):
    name = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name.username}"
    