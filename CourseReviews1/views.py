from django.shortcuts import render, redirect
from django.http import Http404
from users.models import UNIVERSITY_COLLEGE_CHOICES

def homepage(request):
    if request.user.is_authenticated:
        # Redirect authenticated users to their university college homepage
        uc = request.user.university_college
        return redirect(f'/{uc}/courses/')
    
    # For anonymous users, show university college selection
    context = {
        'university_colleges': UNIVERSITY_COLLEGE_CHOICES
    }
    return render(request, 'homepage.html', context)

def university_college_check(request, university_college):
    """
    Middleware-like function to verify the university_college parameter is valid.
    Can be called from views that need to validate the university_college.
    """
    valid_codes = [code for code, name in UNIVERSITY_COLLEGE_CHOICES]
    if university_college not in valid_codes:
        raise Http404(f"University college '{university_college}' not found")
