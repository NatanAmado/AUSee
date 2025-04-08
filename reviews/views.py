from .models import Course, Review, ReviewVote, CourseReport, ReviewReply, ReviewReport
from .forms import ReviewForm, CourseForm, ReviewReplyForm, ReviewReportForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Count, Case, When, Value, IntegerField, Avg
import json
from django.contrib import messages
from CourseReviews1.views import university_college_check

# Create your views here.


@login_required
def course_list(request, university_college):
    # Verify university_college is valid
    university_college_check(request, university_college)
    
    query = request.GET.get('q')
    
    # Start with an optimized queryset that prefetches reviews
    courses = Course.objects.filter(university_college=university_college)
    
    # Only show non-archived courses to regular users
    if not (request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)):
        courses = courses.filter(archived=False)
    
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
        'is_staff_or_superuser': request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff),
        'university_college': university_college
    }

    return render(request, 'reviews/course_list.html', context)

@login_required
def course_detail(request, university_college, course_id):
    course = get_object_or_404(Course, id=course_id, university_college=university_college)
    
    # Redirect regular users if the course is archived
    if course.archived and not (request.user.is_superuser or request.user.is_staff):
        messages.warning(request, "This course has been archived and is not available for viewing.")
        return redirect('reviews:course_list', university_college=university_college)
    
    # Check if the user has already reported this course
    user_reported = False
    if request.user.is_authenticated:
        user_reported = CourseReport.objects.filter(course=course, user=request.user).exists()
    
    # Get the year filter from the query parameters
    current_year = request.GET.get('year', '')
    
    # Get all reviews for this course with vote counts
    reviews = course.review_set.all()
    
    # Only show non-archived reviews to regular users
    if not (request.user.is_superuser or request.user.is_staff):
        reviews = reviews.filter(archived=False)
        
    reviews = reviews.annotate(
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
    
    # Get user votes for reviews
    user_votes = {}
    user_upvoted_reviews = set()
    user_downvoted_reviews = set()
    if request.user.is_authenticated:
        user_vote_objects = ReviewVote.objects.filter(
            user=request.user,
            review__in=reviews
        )
        for vote in user_vote_objects:
            user_votes[vote.review_id] = 'upvote' if vote.is_upvote else 'downvote'
            if vote.is_upvote:
                user_upvoted_reviews.add(vote.review_id)
            else:
                user_downvoted_reviews.add(vote.review_id)
    
    # Initialize reply form
    reply_form = ReviewReplyForm()
    
    if request.method == "POST":
        # Check if this is a delete request
        if 'delete_review' in request.POST:
            review_id = request.POST.get('review_id')
            review_to_delete = get_object_or_404(Review, id=review_id, user=request.user)
            review_to_delete.delete()
            # Redirect to the same page after deletion
            return redirect('reviews:course_detail', university_college=university_college, course_id=course_id)
            
        # Otherwise handle the review creation code
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = request.user  # Set the user for the review
            review.save()
            # Redirect to the same course detail page after adding the review
            return redirect('reviews:course_detail', university_college=university_college, course_id=course_id)
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
        'user_votes': user_votes,
        'user_upvoted_reviews': user_upvoted_reviews,
        'user_downvoted_reviews': user_downvoted_reviews,
        'is_staff_or_superuser': request.user.is_superuser or request.user.is_staff,
        'university_college': university_college
    }

    return render(request, 'reviews/course_detail.html', context)

@login_required
def add_reply(request, university_college, course_id, review_id):
    """Add a reply to a review"""
    course = get_object_or_404(Course, id=course_id, university_college=university_college)
    review = get_object_or_404(Review, id=review_id, course=course)
    
    if request.method == "POST":
        form = ReviewReplyForm(request.POST)
        print(f"Form data: {request.POST}")
        
        # Check if the form is valid
        if form.is_valid():
            reply = form.save(commit=False)
            reply.review = review
            reply.user = request.user
            
            # Set whether the reply is anonymous
            reply.is_anonymous = form.cleaned_data.get('is_anonymous', True)
            
            reply.save()
            
            # Redirect back to the course detail page
            return redirect('reviews:course_detail', university_college=university_college, course_id=course_id)
    
    # If not POST or form invalid, redirect to the course page
    return redirect('reviews:course_detail', university_college=university_college, course_id=course_id)

@login_required
def delete_reply(request, university_college, course_id, reply_id):
    """Delete a reply"""
    course = get_object_or_404(Course, id=course_id, university_college=university_college)
    reply = get_object_or_404(ReviewReply, id=reply_id, user=request.user)
    
    # Delete the reply
    reply.delete()
    
    # Redirect back to the course detail page
    return redirect('reviews:course_detail', university_college=university_college, course_id=course_id)

@login_required
def add_course(request, university_college):
    """Add a new course"""
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.university_college = university_college
            course.save()
            return redirect('reviews:course_detail', university_college=university_college, course_id=course.id)
    else:
        form = CourseForm()
    
    return render(request, 'reviews/add_course.html', {'form': form, 'university_college': university_college})

@login_required
def report_course(request, university_college, course_id):
    """Report a course as not real"""
    course = get_object_or_404(Course, id=course_id, university_college=university_college)
    
    # Check if this is a verified course that cannot be reported
    if course.is_verified():
        messages.error(request, "This course is verified and cannot be reported.")
        return redirect('reviews:course_detail', university_college=university_college, course_id=course_id)
    
    # Check if the user has already reported this course
    if CourseReport.objects.filter(course=course, user=request.user).exists():
        messages.warning(request, "You have already reported this course.")
        return redirect('reviews:course_detail', university_college=university_college, course_id=course_id)
    
    # Process the vote
    vote = request.POST.get('vote', 'not_real')  # Default to 'not_real'
    reason = request.POST.get('reason', '')
    
    # Create the report
    CourseReport.objects.create(
        course=course,
        user=request.user,
        vote=vote,
        reason=reason
    )
    
    # Check if the course should be archived
    if course.should_be_archived():
        course.archived = True
        course.save()
        messages.success(request, "This course has been archived based on user reports.")
    else:
        messages.success(request, "Thank you for your report. It has been recorded.")
    
    # Redirect back to the course list
    return redirect('reviews:course_list', university_college=university_college)

@login_required
def report_review(request, university_college, course_id, review_id):
    """Report a review"""
    course = get_object_or_404(Course, id=course_id, university_college=university_college)
    review = get_object_or_404(Review, id=review_id, course=course)
    
    # Check if the user has already reported this review
    if ReviewReport.objects.filter(review=review, user=request.user).exists():
        messages.warning(request, "You have already reported this review.")
        return redirect('reviews:course_detail', university_college=university_college, course_id=course_id)
    
    if request.method == "POST":
        form = ReviewReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.review = review
            report.user = request.user
            report.save()
            
            # Check if review should be archived
            if review.check_archive_status():
                messages.success(request, "The review has been archived due to multiple reports.")
            else:
                messages.success(request, "Thank you for your report. It has been recorded.")
            
            return redirect('reviews:course_detail', university_college=university_college, course_id=course_id)
    
    messages.error(request, "There was an error processing your report.")
    return redirect('reviews:course_detail', university_college=university_college, course_id=course_id)

def about(request, university_college):
    return render(request, 'reviews/about.html', {'university_college': university_college})


