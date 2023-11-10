from .models import Course, Review
from .forms import ReviewForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.


def course_list(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(Q(name__icontains=query) | Q(code__icontains=query))
    else:
        courses = Course.objects.all()

    level_100_courses = courses.filter(level=100).order_by('name')
    level_200_courses = courses.filter(level=200).order_by('name')
    level_300_courses = courses.filter(level=300).order_by('name')

    context = {
        'level_100_courses': level_100_courses,
        'level_200_courses': level_200_courses,
        'level_300_courses': level_300_courses,
    }

    return render(request, 'reviews/course_list.html', context)




def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    year_filter = request.GET.get('year')
    if year_filter:
        reviews = Review.objects.filter(course=course, created_date__year=year_filter)
    else:
        reviews = Review.objects.filter(course=course)

    years = set(review.created_date.year for review in reviews)

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

    if 'delete_review' in request.POST:
        review_id = request.POST.get('review_id')
        review = Review.objects.get(id=review_id, user=request.user)
        review.delete()
        return HttpResponseRedirect(request.path_info)
    
    context = {
        'course': course,
        'reviews': reviews,
        'form': form,
        'current_year': year_filter,
        'available_years': years
    }

    return render(request, 'reviews/course_detail.html', context)
