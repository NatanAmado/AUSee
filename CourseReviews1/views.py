from django.shortcuts import render, redirect
from django.http import Http404
from users.models import UNIVERSITY_COLLEGE_CHOICES

def homepage(request):
    if request.user.is_authenticated:
        # Redirect authenticated users to their university college homepage
        uc = request.user.university_college
        return redirect(f'/{uc}/courses/')
    
    # Only include the specified university colleges: AUC, UCU, UCR, EUC, UCG, LUC
    filtered_colleges = [(code, name) for code, name in UNIVERSITY_COLLEGE_CHOICES 
                         if code.lower() in ['auc', 'ucu', 'ucr', 'euc', 'ucg', 'luc']]
    
    # For anonymous users, show university college selection with filtered list
    context = {
        'university_colleges': filtered_colleges,
        'show_full_navbar': True,     # Flag to ensure navbar is fully displayed
        'hide_navbar': False          # Explicitly set to false
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

def custom_404_view(request, exception=None):
    """
    Custom 404 view that renders our fancy 404.html template.
    """
    # Get the current university_college from the request path if possible
    path = request.path.strip('/')
    university_college = None
    
    # Try to extract university_college from the path
    if path and '/' in path:
        potential_uc = path.split('/')[0]
        valid_codes = [code for code, name in UNIVERSITY_COLLEGE_CHOICES]
        if potential_uc in valid_codes:
            university_college = potential_uc
    
    # Default to 'auc' if no university_college found
    if not university_college:
        university_college = 'auc'
        
    context = {
        'university_college': university_college,
    }
    
    # Return 404 template with 404 status
    return render(request, '404.html', context, status=404)
