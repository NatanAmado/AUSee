from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F, Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .models import Topic, Post, Comment, Vote, TopicReport, PostReport
from .forms import TopicForm, PostForm, CommentForm, TopicDescriptionForm, TopicReportForm, PostReportForm
from django import forms
from CourseReviews1.views import university_college_check

@login_required
def forum_home(request, university_college):
    """Display the forum homepage with a list of topics"""
    # Verify university_college is valid
    university_college_check(request, university_college)
    
    # Query topics for this university college OR global topics
    topics = Topic.objects.filter(Q(university_college=university_college) | Q(is_global=True))
    
    # Only show non-archived topics to regular users
    if not (request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)):
        topics = topics.filter(is_archived=False)
        recent_posts = Post.objects.filter(
            Q(topic__university_college=university_college) | Q(topic__is_global=True), 
            is_archived=False
        ).order_by('-created_at')[:5]
    else:
        recent_posts = Post.objects.filter(
            Q(topic__university_college=university_college) | Q(topic__is_global=True)
        ).order_by('-created_at')[:5]
    
    context = {
        'topics': topics,
        'recent_posts': recent_posts,
        'is_staff_or_superuser': request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff),
        'university_college': university_college
    }
    return render(request, 'forum/home.html', context)

@login_required
def topic_list(request, university_college):
    """Display a list of all topics"""
    # Include both university-specific topics and global topics
    topics = Topic.objects.filter(Q(university_college=university_college) | Q(is_global=True))
    
    # Only show non-archived topics to regular users
    if not (request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)):
        topics = topics.filter(is_archived=False)
    
    topics = topics.order_by('-is_global', 'name')
    
    context = {
        'topics': topics,
        'is_staff_or_superuser': request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff),
        'university_college': university_college
    }
    return render(request, 'forum/topic_list.html', context)

@login_required
def create_topic(request, university_college):
    """Create a new topic"""
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.created_by = request.user
            topic.university_college = university_college
            topic.save()
            messages.success(request, 'Topic created successfully!')
            return redirect('forum:topic_detail', university_college=university_college, topic_id=topic.id)
    else:
        form = TopicForm()
    
    context = {
        'form': form,
        'title': 'Create New Topic',
        'university_college': university_college
    }
    return render(request, 'forum/topic_form.html', context)

@login_required
def topic_detail(request, university_college, topic_id):
    """Display a topic and its posts"""
    topic = get_object_or_404(Topic, id=topic_id, university_college=university_college)
    
    # Redirect regular users if the topic is archived
    if topic.is_archived and not (request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)):
        messages.warning(request, "This topic has been archived and is not available for viewing.")
        return redirect('forum:home', university_college=university_college)
    
    # Sort posts based on query parameter
    sort_by = request.GET.get('sort', 'recent')
    
    # Base queryset with topic filter
    posts_query = Post.objects.filter(topic=topic)
    
    # Only show non-archived posts to regular users
    if not (request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)):
        posts_query = posts_query.filter(is_archived=False)
    
    if sort_by == 'top':
        # Calculate net votes at the database level
        posts_list = posts_query.annotate(
            net_votes=F('upvotes') - F('downvotes')
        ).order_by('-net_votes', '-created_at')
    else:  # Default is 'recent'
        posts_list = posts_query.order_by('-created_at')
    
    # Paginate posts
    paginator = Paginator(posts_list, 10)  # Show 10 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    # Create post form for the topic page
    form = PostForm(initial={'topic': topic})
    form.fields['topic'].widget = forms.HiddenInput()
    
    context = {
        'topic': topic,
        'posts': posts,
        'form': form,
        'sort_by': sort_by,
        'is_staff_or_superuser': request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff),
        'university_college': university_college
    }
    return render(request, 'forum/topic_detail.html', context)

@login_required
def edit_topic_description(request, university_college, topic_id):
    """Allow any user to edit a topic's description"""
    topic = get_object_or_404(Topic, id=topic_id, university_college=university_college)
    
    if request.method == 'POST':
        form = TopicDescriptionForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Topic description updated successfully!')
            return redirect('forum:topic_detail', university_college=university_college, topic_id=topic.id)
    else:
        form = TopicDescriptionForm(instance=topic)
    
    context = {
        'form': form,
        'topic': topic,
        'title': 'Edit Topic Description',
        'university_college': university_college
    }
    return render(request, 'forum/edit_topic_description.html', context)

@login_required
def report_topic(request, university_college, topic_id):
    """Allow users to report a topic"""
    topic = get_object_or_404(Topic, id=topic_id, university_college=university_college)
    
    # Don't allow reporting already archived topics
    if topic.is_archived:
        messages.warning(request, 'This topic has already been archived.')
        return redirect('forum:topic_detail', university_college=university_college, topic_id=topic.id)
    
    # Check if user already reported this topic
    if TopicReport.objects.filter(topic=topic, user=request.user).exists():
        messages.warning(request, 'You have already reported this topic.')
        return redirect('forum:topic_detail', university_college=university_college, topic_id=topic.id)
    
    if request.method == 'POST':
        form = TopicReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.topic = topic
            report.user = request.user
            report.save()
            
            # Check if topic should be archived
            if topic.check_archive_status():
                messages.warning(request, 'This topic has received multiple reports and has been archived.')
                return redirect('forum:home', university_college=university_college)
            
            daily_report_count = topic.daily_report_count()
            if daily_report_count >= 5:
                messages.info(request, f'This topic has {daily_report_count} reports in the last 24 hours and is being monitored.')
            
            messages.success(request, 'Thank you for your report. We will review this topic.')
            return redirect('forum:topic_detail', university_college=university_college, topic_id=topic.id)
    else:
        form = TopicReportForm()
    
    context = {
        'form': form,
        'topic': topic,
        'title': 'Report Topic',
        'daily_report_count': topic.daily_report_count(),
        'university_college': university_college
    }
    return render(request, 'forum/report_topic.html', context)

@login_required
def create_post(request, university_college, topic_id=None):
    """Create a new post"""
    initial = {}
    topic = None
    if topic_id:
        topic = get_object_or_404(Topic, id=topic_id, university_college=university_college)
        initial['topic'] = topic
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # Ensure the topic belongs to the correct university college
            topic = form.cleaned_data.get('topic')
            if topic.university_college != university_college:
                messages.error(request, 'Invalid topic selection.')
                return redirect('forum:home', university_college=university_college)
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('forum:post_detail', university_college=university_college, post_id=post.id)
    else:
        form = PostForm(initial=initial)
        # Filter topics by university_college
        form.fields['topic'].queryset = Topic.objects.filter(university_college=university_college)
    
    context = {
        'form': form,
        'title': 'Create New Post',
        'university_college': university_college
    }
    return render(request, 'forum/post_form.html', context)

@login_required
def edit_post(request, university_college, post_id):
    """Edit an existing post"""
    post = get_object_or_404(Post, id=post_id, topic__university_college=university_college)
    
    # Only allow the author to edit the post
    if post.author != request.user:
        messages.error(request, 'You can only edit your own posts.')
        return redirect('forum:post_detail', university_college=university_college, post_id=post.id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('forum:post_detail', university_college=university_college, post_id=post.id)
    else:
        form = PostForm(instance=post)
        # Filter topics by university_college
        form.fields['topic'].queryset = Topic.objects.filter(university_college=university_college)
    
    context = {
        'form': form,
        'title': 'Edit Post',
        'post': post,
        'university_college': university_college
    }
    return render(request, 'forum/post_form.html', context)

@login_required
def post_detail(request, university_college, post_id):
    """Display a post and its comments"""
    post = get_object_or_404(Post, id=post_id, topic__university_college=university_college)
    
    # Redirect regular users if the post is archived
    if post.is_archived and not (request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)):
        messages.warning(request, "This post has been archived and is not available for viewing.")
        return redirect('forum:topic_detail', university_college=university_college, topic_id=post.topic.id)
    
    # Get all comments for the post
    comments = Comment.objects.filter(post=post, parent=None).prefetch_related('replies')
    
    # Get user vote if any
    user_vote = None
    if request.user.is_authenticated:
        try:
            vote = Vote.objects.get(user=request.user, post=post)
            user_vote = vote.vote_type
        except Vote.DoesNotExist:
            pass
    
    # Check if user already reported this post
    user_reported = False
    if request.user.is_authenticated:
        user_reported = PostReport.objects.filter(post=post, user=request.user).exists()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': CommentForm(),
        'user_vote': user_vote,
        'user_reported': user_reported,
        'is_staff_or_superuser': request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff),
        'university_college': university_college
    }
    return render(request, 'forum/post_detail.html', context)

@login_required
@require_POST
def add_comment(request, university_college, post_id):
    """Add a comment to a post"""
    post = get_object_or_404(Post, id=post_id, topic__university_college=university_college)
    parent_id = request.POST.get('parent_id')
    
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        
        # Handle replies to existing comments
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id, post=post)
                comment.parent = parent_comment
            except Comment.DoesNotExist:
                pass
            
        comment.save()
        messages.success(request, 'Comment added successfully!')
    else:
        messages.error(request, 'Error adding comment. Please try again.')
    
    return redirect('forum:post_detail', university_college=university_college, post_id=post.id)

@login_required
@require_POST
def vote_post(request, university_college, post_id):
    """Handle upvoting and downvoting of posts"""
    post = get_object_or_404(Post, id=post_id, topic__university_college=university_college)
    vote_type = request.POST.get('vote_type')
    
    if vote_type not in ['upvote', 'downvote']:
        return JsonResponse({'status': 'error', 'message': 'Invalid vote type'})
    
    # Check if the user has already voted on this post
    try:
        # User has already voted, get their vote
        vote = Vote.objects.get(user=request.user, post=post)
        old_vote_type = vote.vote_type
        
        # If the same vote type, remove the vote (toggle off)
        if vote_type == old_vote_type:
            # Undo the vote count
            if old_vote_type == 'upvote':
                post.upvotes = F('upvotes') - 1
            else:
                post.downvotes = F('downvotes') - 1
            post.save()
            vote.delete()
            
            # Refresh the post object to get updated values
            post.refresh_from_db()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Vote removed',
                'upvotes': post.upvotes,
                'downvotes': post.downvotes,
                'user_vote': None
            })
        else:
            # Change vote type, update counters
            if old_vote_type == 'upvote':
                # Change from upvote to downvote
                post.upvotes = F('upvotes') - 1
                post.downvotes = F('downvotes') + 1
            else:
                # Change from downvote to upvote
                post.downvotes = F('downvotes') - 1
                post.upvotes = F('upvotes') + 1
            
            vote.vote_type = vote_type
            vote.save()
            post.save()
            
            # Refresh the post object
            post.refresh_from_db()
            
            # Check if the post should be archived due to negative votes
            post.check_archive_status()
            
            return JsonResponse({
                'status': 'success',
                'message': f'Vote changed to {vote_type}',
                'upvotes': post.upvotes,
                'downvotes': post.downvotes,
                'user_vote': vote_type
            })
            
    except Vote.DoesNotExist:
        # User hasn't voted yet, create a new vote
        vote = Vote(user=request.user, post=post, vote_type=vote_type)
        vote.save()
        
        # Update the post's vote count
        if vote_type == 'upvote':
            post.upvotes = F('upvotes') + 1
        else:
            post.downvotes = F('downvotes') + 1
        post.save()
        
        # Refresh the post object
        post.refresh_from_db()
        
        # Check if the post should be archived due to negative votes
        post.check_archive_status()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Post {vote_type}d successfully',
            'upvotes': post.upvotes,
            'downvotes': post.downvotes,
            'user_vote': vote_type
        })

@login_required
def search_forum(request, university_college):
    """Search for posts and topics"""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')
    
    # Initialize empty queryset
    topics = Topic.objects.none()
    posts = Post.objects.none()
    
    if query:
        # Filter by university_college for all searches
        if search_type == 'topics' or search_type == 'all':
            topics = Topic.objects.filter(
                university_college=university_college,
                name__icontains=query
            )
            # Only show non-archived topics to regular users
            if not (request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)):
                topics = topics.filter(is_archived=False)
        
        if search_type == 'posts' or search_type == 'all':
            # Filter posts by both title and content
            posts = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query),
                topic__university_college=university_college
            )
            # Only show non-archived posts to regular users
            if not (request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)):
                posts = posts.filter(is_archived=False)
    
    context = {
        'query': query,
        'topics': topics,
        'posts': posts,
        'search_type': search_type,
        'university_college': university_college
    }
    return render(request, 'forum/search_results.html', context)

@login_required
def report_post(request, university_college, post_id):
    """Allow users to report a post"""
    post = get_object_or_404(Post, id=post_id, topic__university_college=university_college)
    
    # Don't allow reporting already archived posts
    if post.is_archived:
        messages.warning(request, 'This post has already been archived.')
        return redirect('forum:post_detail', university_college=university_college, post_id=post_id)
    
    # Check if user already reported this post
    if PostReport.objects.filter(post=post, user=request.user).exists():
        messages.warning(request, 'You have already reported this post.')
        return redirect('forum:post_detail', university_college=university_college, post_id=post_id)
    
    if request.method == 'POST':
        form = PostReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.post = post
            report.user = request.user
            report.save()
            
            # Check if post should be archived
            if post.check_archive_status():
                messages.warning(request, 'This post has received multiple reports and has been archived.')
            else:
                messages.success(request, 'Thank you for your report. We will review this post.')
            
            return redirect('forum:post_detail', university_college=university_college, post_id=post_id)
    else:
        form = PostReportForm()
    
    context = {
        'form': form,
        'post': post,
        'title': 'Report Post',
        'university_college': university_college
    }
    return render(request, 'forum/report_post.html', context)

@login_required
def create_post_in_topic(request, university_college, topic_id):
    """Create a new post in a specific topic"""
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Redirect regular users if the topic is archived
    if topic.is_archived and not (request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)):
        messages.warning(request, "This topic has been archived and is not available for posting.")
        return redirect('forum:home', university_college=university_college)
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.topic = topic
            
            # For global topics, posts should have the author's university college
            if topic.is_global:
                post.author_university_college = request.user.university_college
                
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('forum:post_detail', university_college=university_college, post_id=post.id)
    else:
        form = PostForm(initial={'topic': topic})
        form.fields['topic'].widget = forms.HiddenInput()
    
    context = {
        'form': form,
        'topic': topic,
        'title': 'Create New Post',
        'university_college': university_college
    }
    return render(request, 'forum/post_form.html', context)
