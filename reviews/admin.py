from django.contrib import admin
from .models import Course, Review, ReviewVote, ReviewReply

class ReviewInline(admin.TabularInline):  
    model = Review
    extra = 0  # Number of empty forms to display; set to 0 to only show existing reviews

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'level')
    list_filter = ('level', )
    search_fields = ('name', 'code')
    inlines = [ReviewInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'rating', 'text', 'created_date')
    list_filter = ('course', 'rating', 'created_date')
    search_fields = ('text', 'course__name')

@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'is_upvote')
    list_filter = ('is_upvote', )
    search_fields = ('user__username', 'review__text')

@admin.register(ReviewReply)
class ReviewReplyAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'text', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('text', 'user__username', 'review__text')
