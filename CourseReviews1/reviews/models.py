from django.db import models

# Create your models here.

LEVEL_CHOICES = [
    (100, '100 Level'),
    (200, '200 Level'),
    (300, '300 Level'),
]

RATING_CHOICES = [(i / 10, f"{i / 10}") for i in range(10, 101)]


class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
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

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.DecimalField(choices=RATING_CHOICES, max_digits=3, decimal_places=1)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.course.name}"
