from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import math
from datetime import timedelta
from users.models import UNIVERSITY_COLLEGE_CHOICES

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_topics')
    is_archived = models.BooleanField(default=False)
    university_college = models.CharField(max_length=4, choices=UNIVERSITY_COLLEGE_CHOICES, default='auc')
    is_global = models.BooleanField(default=False, help_text="If True, this topic is visible to all university colleges")
    
    def __str__(self):
        return self.name
    
    def report_count(self):
        return self.reports.count()
    
    def daily_report_count(self):
        """Count reports from the last 24 hours"""
        one_day_ago = timezone.now() - timedelta(days=1)
        return self.reports.filter(created_at__gte=one_day_ago).count()
    
    def should_be_archived(self):
        """Archive topic if it has 10+ reports in a single day"""
        return self.daily_report_count() >= 10
    
    def check_archive_status(self):
        """Check if topic should be archived and archive it along with all its posts if needed"""
        if self.should_be_archived() and not self.is_archived:
            self.is_archived = True
            self.save()
            
            # Archive all posts in this topic
            self.posts.update(is_archived=True)
            return True
        return False
    
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'university_college']  # Name only needs to be unique within a university college

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    is_anonymous = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    author_university_college = models.CharField(max_length=4, blank=True, null=True)
    
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
    
    def should_be_archived(self):
        """Archive post if downvotes exceed upvotes by 10 or more"""
        return (self.downvotes - self.upvotes) >= 10 or self.report_count() >= 5
    
    def report_count(self):
        """Count the number of reports for this post"""
        return self.reports.count()
    
    def check_archive_status(self):
        """Check and update the archive status based on votes or reports"""
        if self.should_be_archived() and not self.is_archived:
            self.is_archived = True
            self.save()
            return True
        return False
    
    class Meta:
        ordering = ['-created_at']

class PostReport(models.Model):
    REPORT_REASONS = [
        ('inappropriate', 'Inappropriate Content'),
        ('spam', 'Spam'),
        ('offensive', 'Offensive Content'),
        ('false', 'False Information'),
        ('other', 'Other'),
    ]
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS, default='other')
    additional_info = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')  # Prevent multiple reports from same user
    
    def __str__(self):
        return f"Report on post '{self.post.title}' by {self.user.username}"

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
