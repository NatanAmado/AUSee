from django.db import models
from profanity import profanity
from users.models import CustomUser

# Create your models here.

LEVEL_CHOICES = [
    (100, '100 Level'),
    (200, '200 Level'),
    (300, '300 Level'),
]

RATING_CHOICES = [(i / 10, f"{i / 10}") for i in range(10, 51)]


class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=100)


    def average_rating(self):
        # Get all reviews for this course
        reviews = self.review_set.all()

        # Return None if there are no reviews
        if not reviews:
            return None

        # Calculate the average rating
        total_rating = sum([review.rating for review in reviews])
        avg_rating = total_rating / len(reviews)
        
        return round(avg_rating, 1)  # round to 1 decimal place



    def __str__(self):
        return self.name
    
profanity.set_censor_characters('****')

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.FloatField(choices=RATING_CHOICES)
    teacher_name = models.CharField(max_length=100, blank = True, null = True)
    teacher_quality = models.FloatField(choices=RATING_CHOICES, blank = True, null = True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)



    def save(self, *args, **kwargs):
        # Clean the review text before saving
        self.text = profanity.censor(self.text)
        super(Review, self).save(*args, **kwargs)

    def __str__(self):
        return f"Review for {self.course.name}"
