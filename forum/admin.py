from django.contrib import admin
from .models import Topic, Post, Comment, Vote, TopicReport, PostReport

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'created_by')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'author', 'is_anonymous', 'created_at', 'upvotes', 'downvotes', 'is_archived')
    list_filter = ('topic', 'is_anonymous', 'is_archived', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('upvotes', 'downvotes')
    actions = ['archive_posts', 'unarchive_posts']
    
    def archive_posts(self, request, queryset):
        queryset.update(is_archived=True)
    archive_posts.short_description = "Archive selected posts"
    
    def unarchive_posts(self, request, queryset):
        queryset.update(is_archived=False)
    unarchive_posts.short_description = "Unarchive selected posts"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'post', 'author', 'is_anonymous', 'created_at')
    list_filter = ('is_anonymous', 'created_at')
    search_fields = ('content',)

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'vote_type', 'created_at')
    list_filter = ('vote_type', 'created_at')
    search_fields = ('user__username', 'post__title')

@admin.register(PostReport)
class PostReportAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'reason', 'created_at')
    list_filter = ('reason', 'created_at')
    search_fields = ('post__title', 'user__username', 'additional_info')
