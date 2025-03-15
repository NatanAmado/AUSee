from django.contrib import admin
from .models import Course, Review, ReviewVote, CourseReport, ReviewReply, ReviewReport

class ReviewInline(admin.TabularInline):  
    model = Review
    extra = 0  # Number of empty forms to display; set to 0 to only show existing reviews

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'level', 'average_rating', 'archived')
    list_filter = ('level', 'archived')
    search_fields = ('name', 'code')
    inlines = [ReviewInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_date', 'archived')
    list_filter = ('rating', 'created_date', 'archived')
    search_fields = ('text', 'course__name', 'user__username')

@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'is_upvote')
    list_filter = ('is_upvote',)
    search_fields = ('user__username', 'review__text')

@admin.register(CourseReport)
class CourseReportAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'vote', 'created_at')
    list_filter = ('vote', 'created_at')
    search_fields = ('course__name', 'user__username', 'reason')

@admin.register(ReviewReply)
class ReviewReplyAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'created_date', 'is_anonymous')
    list_filter = ('created_date', 'is_anonymous')
    search_fields = ('text', 'user__username')

@admin.register(ReviewReport)
class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'reason', 'created_at')
    list_filter = ('reason', 'created_at')
    search_fields = ('review__text', 'user__username', 'additional_info')
