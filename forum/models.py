from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import math

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_topics')
    
    def __str__(self):
        return self.name
    
    def report_count(self):
        return self.reports.count()
    
    def should_be_archived(self):
        # Archive topic if it has more than 5 reports
        return self.report_count() >= 5
    
    class Meta:
        ordering = ['name']

class TopicReport(models.Model):
    REPORT_REASONS = [
        ('inappropriate', 'Inappropriate Content'),
        ('spam', 'Spam'),
        ('duplicate', 'Duplicate Topic'),
        ('offensive', 'Offensive Content'),
        ('other', 'Other'),
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS, default='other')
    additional_info = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('topic', 'user')  # Prevent multiple reports from same user
    
    def __str__(self):
        return f"Report on {self.topic.name} by {self.user.username}"

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='posts')
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    is_archived = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    @property
    def score(self):
        # Wilson score interval for sorting
        # This gives better results than a simple upvotes - downvotes
        n = self.upvotes + self.downvotes
        if n == 0:
            return 0
        
        z = 1.96  # 95% confidence
        p = float(self.upvotes) / n
        
        # Wilson score interval
        numerator = p + z*z/(2*n) - z * math.sqrt((p*(1-p) + z*z/(4*n))/n)
        denominator = 1 + z*z/n
        
        return numerator / denominator
    
    def check_archive_status(self):
        # Archive posts with a significant number of downvotes
        # This is a simple implementation - can be adjusted based on requirements
        if self.downvotes > 10 and self.downvotes > self.upvotes * 2:
            self.is_archived = True
            self.save()
    
    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='comments')
    is_anonymous = models.BooleanField(default=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    def __str__(self):
        return f"Comment by {self.author.username if self.author and not self.is_anonymous else 'Anonymous'}"
    
    class Meta:
        ordering = ['created_at']

class Vote(models.Model):
    VOTE_TYPES = (
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='vote_records')
    vote_type = models.CharField(max_length=10, choices=VOTE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Ensure a user can only vote once per post
        unique_together = ('user', 'post')
