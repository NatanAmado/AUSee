from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F, Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .models import Topic, Post, Comment, Vote
from .forms import TopicForm, PostForm, CommentForm

def forum_home(request):
    """Display the forum homepage with a list of topics"""
    topics = Topic.objects.all()
    recent_posts = Post.objects.filter(is_archived=False).order_by('-created_at')[:5]
    
    context = {
        'topics': topics,
        'recent_posts': recent_posts,
    }
    return render(request, 'forum/home.html', context)

def topic_list(request):
    """Display a list of all topics"""
    topics = Topic.objects.all()
    
    context = {
        'topics': topics,
    }
    return render(request, 'forum/topic_list.html', context)

@login_required
def create_topic(request):
    """Create a new topic"""
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.created_by = request.user
            topic.save()
            messages.success(request, 'Topic created successfully!')
            return redirect('forum:topic_detail', topic_id=topic.id)
    else:
        form = TopicForm()
    
    context = {
        'form': form,
        'title': 'Create New Topic',
    }
    return render(request, 'forum/topic_form.html', context)

def topic_detail(request, topic_id):
    """Display a topic and its posts"""
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Filter posts
    sort_by = request.GET.get('sort', 'recent')
    if sort_by == 'top':
        # Sort by score (using the property)
        posts_list = sorted(
            Post.objects.filter(topic=topic, is_archived=False),
            key=lambda p: p.score,
            reverse=True
        )
    else:  # Default to recent
        posts_list = Post.objects.filter(topic=topic, is_archived=False).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(posts_list, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    # Create post form
    form = PostForm(initial={'topic': topic})
    
    context = {
        'topic': topic,
        'posts': posts,
        'form': form,
        'sort_by': sort_by,
    }
    return render(request, 'forum/topic_detail.html', context)

@login_required
def create_post(request, topic_id=None):
    """Create a new post"""
    initial = {}
    topic = None
    if topic_id:
        topic = get_object_or_404(Topic, id=topic_id)
        initial['topic'] = topic
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('forum:post_detail', post_id=post.id)
    else:
        form = PostForm(initial=initial)
    
    context = {
        'form': form,
        'title': 'Create New Post',
        'topic': topic,
    }
    return render(request, 'forum/post_form.html', context)

@login_required
def edit_post(request, post_id):
    """Edit an existing post"""
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user is the author
    if post.author != request.user:
        messages.error(request, "You can't edit someone else's post.")
        return redirect('forum:post_detail', post_id=post.id)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('forum:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'title': 'Edit Post',
        'post': post,
    }
    return render(request, 'forum/post_form.html', context)

def post_detail(request, post_id):
    """Display a post and its comments"""
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post, parent=None).order_by('created_at')
    
    # Comment form
    form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'forum/post_detail.html', context)

@login_required
@require_POST
def add_comment(request, post_id):
    """Add a comment to a post"""
    post = get_object_or_404(Post, id=post_id)
    
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        
        # Prevent nested replies
        parent_id = request.POST.get('parent_id')
        if parent_id:
            messages.error(request, 'Nested replies are not allowed.')
            return redirect('forum:post_detail', post_id=post.id)
        
        comment.save()
        messages.success(request, 'Comment added successfully!')
    else:
        messages.error(request, 'Error adding comment. Please try again.')
    
    return redirect('forum:post_detail', post_id=post.id)

@login_required
@require_POST
def vote_post(request, post_id):
    """Vote on a post (upvote or downvote)"""
    post = get_object_or_404(Post, id=post_id)
    vote_type = request.POST.get('vote_type')
    
    print(f"Vote request received - Post: {post_id}, Type: {vote_type}, User: {request.user.username}")
    
    if vote_type not in ['upvote', 'downvote']:
        return JsonResponse({'status': 'error', 'message': 'Invalid vote type'})
    
    try:
        # Check if user has already voted
        existing_vote = Vote.objects.filter(user=request.user, post=post).first()
        
        if existing_vote:
            print(f"Existing vote found - Type: {existing_vote.vote_type}")
            # User is changing their vote
            if existing_vote.vote_type != vote_type:
                # Update vote counters
                if vote_type == 'upvote':
                    post.upvotes = F('upvotes') + 1
                    post.downvotes = F('downvotes') - 1
                else:
                    post.upvotes = F('upvotes') - 1
                    post.downvotes = F('downvotes') + 1
                
                # Update vote record
                existing_vote.vote_type = vote_type
                existing_vote.save()
                print(f"Vote changed from {existing_vote.vote_type} to {vote_type}")
            else:
                # User is removing their vote
                if vote_type == 'upvote':
                    post.upvotes = F('upvotes') - 1
                else:
                    post.downvotes = F('downvotes') - 1
                
                existing_vote.delete()
                print("Vote removed")
        else:
            # New vote
            if vote_type == 'upvote':
                post.upvotes = F('upvotes') + 1
            else:
                post.downvotes = F('downvotes') + 1
            
            # Create vote record
            Vote.objects.create(
                user=request.user,
                post=post,
                vote_type=vote_type
            )
            print(f"New vote recorded - Type: {vote_type}")
        
        # Save and refresh to get updated counts
        post.save()
        post.refresh_from_db()
        
        # Check if post should be archived
        post.check_archive_status()
        
        print(f"Final vote counts - Upvotes: {post.upvotes}, Downvotes: {post.downvotes}")
        
        return JsonResponse({
            'status': 'success',
            'upvotes': post.upvotes,
            'downvotes': post.downvotes,
            'is_archived': post.is_archived
        })
        
    except Exception as e:
        print(f"Error processing vote: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Error processing vote'
        })

def search_forum(request):
    """Search for posts and topics"""
    query = request.GET.get('q', '')
    
    if query:
        topics = Topic.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(topic__name__icontains=query)
        ).filter(is_archived=False)
    else:
        topics = Topic.objects.none()
        posts = Post.objects.none()
    
    context = {
        'query': query,
        'topics': topics,
        'posts': posts,
    }
    return render(request, 'forum/search_results.html', context)
