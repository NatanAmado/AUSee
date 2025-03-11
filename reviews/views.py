from .models import Course, Review, ReviewVote, CourseReport
from .forms import ReviewForm, CourseForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Max, Min, Avg, Count
import json

# Create your views here.



def course_list(request):
    query = request.GET.get('q')
    
    # Start with an optimized queryset that prefetches reviews
    courses = Course.objects.all()
    
    if query:
        courses = courses.filter(Q(name__icontains=query) | Q(code__icontains=query))
    
    # Add annotations for average rating and review count using the correct relationship
    courses = courses.annotate(
        avg_rating=Avg('review__rating'),  # Using the model name 'review'
        review_count=Count('review')       # Using the model name 'review'
    ).prefetch_related('review_set')
    
    # Split into levels with ordering
    level_100_courses = courses.filter(level=100).order_by('name')
    level_200_courses = courses.filter(level=200).order_by('name')
    level_300_courses = courses.filter(level=300).order_by('name')

    context = {
        'level_100_courses': level_100_courses,
        'level_200_courses': level_200_courses,
        'level_300_courses': level_300_courses,
    }

    return render(request, 'reviews/course_list.html', context)

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if the user has already reported this course
    user_reported = False
    if request.user.is_authenticated:
        user_reported = CourseReport.objects.filter(course=course, user=request.user).exists()
    
    # Get the year filter from the query parameters
    current_year = request.GET.get('year', '')
    
    # Get all reviews for this course
    reviews = course.review_set.all().order_by('-created_date')
    
    # Apply year filter if provided
    if current_year:
        reviews = reviews.filter(created_date__year=current_year)
    
    # Get all available years for filtering
    available_years = Review.objects.filter(course=course).dates('created_date', 'year').values_list('created_date__year', flat=True)
    
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = request.user  # Set the user for the review
            review.save()
            # Redirect to the same course detail page after adding the review
            return redirect('reviews:course_detail', course_id=course_id)
    else:
        form = ReviewForm()

    if 'vote' in request.POST:
        review_id = request.POST.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        vote_type = request.POST.get('vote')  # 'upvote' or 'downvote'
        is_upvote = True if vote_type == 'upvote' else False

        # Check if the user has already voted
        existing_vote = ReviewVote.objects.filter(user=request.user, review=review).first()
        if existing_vote:
            # User has already voted, update vote if different
            if existing_vote.is_upvote != is_upvote:
                existing_vote.is_upvote = is_upvote
                existing_vote.save()  
        else:
            # Create a new vote
            ReviewVote.objects.create(user=request.user, review=review, is_upvote=is_upvote)

        return HttpResponseRedirect(request.path_info)


    
    context = {
        'course': course,
        'reviews': reviews,
        'form': form,
        'current_year': current_year,
        'available_years': available_years,
        'user_reported': user_reported,
    }

    return render(request, 'reviews/course_detail.html', context)


@login_required
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect('reviews:course_detail', course_id=course.id)
    else:
        form = CourseForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'reviews/add_course.html', context)


@login_required
def report_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            vote_type = data.get('vote', 'not_real')  # Default to not_real for backward compatibility
        except:
            vote_type = 'not_real'  # Default if JSON parsing fails
        
        # Check if user already reported this course
        if not CourseReport.objects.filter(course=course, user=request.user).exists():
            # Temporarily use a simpler approach without the vote field
            report = CourseReport(
                course=course,
                user=request.user,
                reason=f"User voted: {vote_type}"
            )
            report.save()
            
            # Check if course should be archived based on report count
            if course.report_count() >= 5 and not course.archived:
                course.archived = True
                course.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'Thank you for your feedback. Your vote has been recorded.'
            })
        else:
            return JsonResponse({
                'success': False, 
                'message': 'You have already voted on this course.'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


