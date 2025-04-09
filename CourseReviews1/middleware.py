from django.shortcuts import redirect
from django.contrib import messages
from django.urls import resolve, reverse
import re

class UniversityCollegeAccessMiddleware:
    """
    Middleware to check if a user has access to the requested university college content.
    Staff and superusers have access to all university colleges.
    Regular users can only access their own university college.
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
                
                # Check if the user has access to this university college
                if url_university_college != user_university_college:
                    messages.error(request, f"You don't have access to {url_university_college.upper()} content.")
                    return redirect(f'/{user_university_college}/courses/')
        
        # Continue processing the request
        response = self.get_response(request)
        return response 