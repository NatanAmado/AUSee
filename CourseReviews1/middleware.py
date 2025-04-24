from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import resolve, reverse
import re
from forum.models import Topic, Post

class UniversityCollegeAccessMiddleware:
    """
    Middleware to check if a user has access to the requested university college content.
    Staff and superusers have access to all university colleges.
    Regular users can only access their own university college.
    Exception: Global topics in the forum are accessible to all users.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Process the request
        if request.user.is_authenticated:
            # Skip middleware for admin and non-university-college URLs
            if request.path.startswith('/admin/') or request.path == '/' or \
               request.path.startswith('/users/login/') or request.path.startswith('/users/register/'):
                return self.get_response(request)
            
            # Extract university_college from the URL
            match = re.match(r'^/([^/]+)/', request.path)
            if match:
                url_university_college = match.group(1)
                user_university_college = request.user.university_college
                
                # Staff and superusers can access all university colleges
                if request.user.is_staff or request.user.is_superuser:
                    return self.get_response(request)
                
                # Allow access to global forum topics regardless of university_college
                if '/forum/' in request.path:
                    # Always allow access to forum home page for listing global topics
                    if request.path.endswith('/forum/') or request.path.endswith('/forum/topics/'):
                        return self.get_response(request)
                    
                    # Extract topic_id or post_id from URL path
                    topic_match = re.search(r'/topics/(\d+)/', request.path)
                    post_match = re.search(r'/posts/(\d+)/', request.path)
                    
                    if topic_match:
                        try:
                            topic_id = int(topic_match.group(1))
                            topic = Topic.objects.get(id=topic_id)
                            if topic.is_global:
                                return self.get_response(request)
                        except (Topic.DoesNotExist, ValueError):
                            pass
                    
                    if post_match:
                        try:
                            post_id = int(post_match.group(1))
                            post = Post.objects.select_related('topic').get(id=post_id)
                            if post.topic.is_global:
                                return self.get_response(request)
                        except (Post.DoesNotExist, ValueError):
                            pass
                
                # Check if the user has access to this university college
                if url_university_college != user_university_college:
                    messages.error(request, f"You don't have access to {url_university_college.upper()} content.")
                    return redirect(f'/{user_university_college}/courses/')
        
        # Continue processing the request
        response = self.get_response(request)
        return response 