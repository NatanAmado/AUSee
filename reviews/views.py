from .models import Course, Review, ReviewVote, CourseReport, ReviewReply, ReviewReport
from .forms import ReviewForm, CourseForm, ReviewReplyForm, ReviewReportForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Count, Case, When, Value, IntegerField, Avg
import json
from django.contrib import messages

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
    
    # Get all reviews for this course with vote counts
    reviews = course.review_set.all().annotate(
        upvotes=Count(
            Case(
                When(reviewvote__is_upvote=True, then=1),
                output_field=IntegerField(),
            )
        ),
        downvotes=Count(
            Case(
                When(reviewvote__is_upvote=False, then=1),
                output_field=IntegerField(),
            )
        )
    ).annotate(
        net_votes=F('upvotes') - F('downvotes')
    ).order_by('-net_votes', '-created_date')
    
    # Apply year filter if provided
    if current_year:
        reviews = reviews.filter(created_date__year=current_year)
    
    # Get all available years for filtering
    available_years = Review.objects.filter(course=course).dates('created_date', 'year').values_list('created_date__year', flat=True)
    
    # Prefetch review replies to avoid N+1 query problem
    reviews = reviews.prefetch_related('replies__user')
    
    # Check which reviews the user has already reported
    reported_reviews = set()
    if request.user.is_authenticated:
        reported_reviews = set(ReviewReport.objects.filter(
            user=request.user, 
            review__in=reviews
        ).values_list('review_id', flat=True))
    
    # Initialize reply form
    reply_form = ReviewReplyForm()
    
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
        'reply_form': reply_form,
        'current_year': current_year,
        'available_years': available_years,
        'user_reported': user_reported,
        'reported_reviews': reported_reviews,
    }

    return render(request, 'reviews/course_detail.html', context)

@login_required
def add_reply(request, course_id, review_id):
    """Add a reply to a review"""
    course = get_object_or_404(Course, id=course_id)
    review = get_object_or_404(Review, id=review_id, course=course)
    
    if request.method == "POST":
        form = ReviewReplyForm(request.POST)
        print(f"Form data: {request.POST}")
        
        # Check if the form is valid
        if form.is_valid():
            reply = form.save(commit=False)
            reply.review = review
            reply.user = request.user
            
            # Get the is_anonymous value directly from POST data
            # Checkbox will only be in POST data if it's checked
            reply.is_anonymous = 'is_anonymous' in request.POST
            print(f"Is anonymous: {reply.is_anonymous}")
            
            reply.save()
            print(f"Reply saved with is_anonymous={reply.is_anonymous}")
            
    # Redirect back to the course detail page
    return redirect('reviews:course_detail', course_id=course_id)

@login_required
def delete_reply(request, course_id, reply_id):
    """Delete a reply"""
    course = get_object_or_404(Course, id=course_id)
    reply = get_object_or_404(ReviewReply, id=reply_id, review__course=course)
    
    # Check if the user is the author of the reply
    if reply.user == request.user:
        reply.delete()
    
    # Redirect back to the course detail page
    return redirect('reviews:course_detail', course_id=course_id)

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

@login_required
def report_review(request, course_id, review_id):
    """Handle reporting a review"""
    course = get_object_or_404(Course, id=course_id)
    review = get_object_or_404(Review, id=review_id, course=course)
    
    # Check if user already reported this review
    if ReviewReport.objects.filter(review=review, user=request.user).exists():
        messages.warning(request, "You have already reported this review.")
        return redirect('reviews:course_detail', course_id=course_id)
    
    if request.method == "POST":
        form = ReviewReportForm(request.POST)
        if form.is_valid():
            # Create the report
            report = form.save(commit=False)
            report.review = review
            report.user = request.user
            report.save()
            
            # Check if review should be archived based on report count
            if review.report_count() >= 5 and not review.archived:
                review.archived = True
                review.save()
            
            return JsonResponse({'success': True, 'message': 'Thank you for your report. This review will be reviewed by our team.'})
        else:
            return JsonResponse({'success': False, 'message': 'There was an error with your report. Please try again.'})
    else:
        form = ReviewReportForm()
    
    return render(request, 'reviews/report_review.html', {'form': form, 'review': review, 'course': course})


