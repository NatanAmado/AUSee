from django.db import models
from profanity import profanity
from users.models import CustomUser
import math
import math
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

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
    archived = models.BooleanField(default=False)


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

    def is_verified(self):
        """Check if this is a verified course that cannot be reported"""
        return self.id <= 328

    def __str__(self):
        return self.name
    
    def report_count(self):
        return self.reports.count()
    
    def real_votes(self):
        return self.reports.filter(vote='real').count()
    
    def not_real_votes(self):
        return self.reports.filter(vote='not_real').count()
    
    def vote_difference(self):
        return self.not_real_votes() - self.real_votes()
        
    def should_be_archived(self):
        return self.vote_difference() >= 5 and not self.archived
    
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
    archived = models.BooleanField(default=False)
    # upvotes and downvotes

    
    def upvote_count(self):
        return self.reviewvote_set.filter(is_upvote=True).count()

    def downvote_count(self):
        return self.reviewvote_set.filter(is_upvote=False).count()

    def save(self, *args, **kwargs):
        # Clean the review text before saving
        self.text = profanity.censor(self.text)
        super(Review, self).save(*args, **kwargs)
        
    def net_votes(self):
        x = self.upvote_count() - self.downvote_count()
        if x < 0:
            return math.floor(x)
        if x > 0:
            return math.ceil(x)
        else:
            return 0
            
    def report_count(self):
        return self.reports.count()
        
    def should_be_archived(self):
        return self.report_count() >= 5 and not self.archived
        
    def check_archive_status(self):
        """Check if review should be archived and update its status if needed"""
        if self.should_be_archived():
            self.archived = True
            self.save(update_fields=['archived'])
            return True
        return False

    def __str__(self):
        return f"Review for {self.course.name}"
    
class ReviewVote(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()  # True for upvote, False for downvote

    class Meta:
        unique_together = ['user', 'review']  # Ensures a user can only vote once per review

class ReviewReply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_anonymous = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        # Clean the reply text before saving
        self.text = profanity.censor(self.text)
        super(ReviewReply, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"Reply to review {self.review.id} by {self.user.username}"
    
    class Meta:
        ordering = ['created_date']
        verbose_name_plural = 'Review Replies'

class ReviewReport(models.Model):
    REPORT_REASONS = [
        ('inappropriate', 'Inappropriate Content'),
        ('spam', 'Spam'),
        ('offensive', 'Offensive Content'),
        ('false', 'False Information'),
        ('other', 'Other'),
    ]
    
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS, default='other')
    additional_info = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('review', 'user')  # Prevent multiple reports from same user
    
    def __str__(self):
        return f"Report on review {self.review.id} by {self.user.username}"

class CourseReport(models.Model):
    VOTE_CHOICES = [
        ('real', 'Course is real'),
        ('not_real', 'Course is not real'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES, default='not_real')
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('course', 'user')  # Prevent multiple reports from same user
        
    def __str__(self):
        return f"Report for {self.course.name} by {self.user.username}: {self.get_vote_display()}"

@login_required
def report_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == "POST":
        form = CourseReportForm(request.POST)
        if form.is_valid():
            # Check if user already reported this course
            if not CourseReport.objects.filter(course=course, user=request.user).exists():
                report = form.save(commit=False)
                report.course = course
                report.user = request.user
                report.save()
                
                # Check if course should be archived
                if course.should_be_archived():
                    course.archived = True
                    course.save()
                
                return JsonResponse({'success': True, 'message': 'Thank you for your report.'})
            else:
                return JsonResponse({'success': False, 'message': 'You have already reported this course.'})
    else:
        form = CourseReportForm()
    
    return render(request, 'reviews/report_course.html', {'form': form, 'course': course})

