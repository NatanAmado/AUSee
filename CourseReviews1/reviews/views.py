from .models import Course, Review
from .forms import ReviewForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect


# Create your views here.


def course_list(request):
    level_100_courses = Course.objects.filter(level=100)
    level_200_courses = Course.objects.filter(level=200)
    level_300_courses = Course.objects.filter(level=300)

    context = {
        'level_100_courses': level_100_courses,
        'level_200_courses': level_200_courses,
        'level_300_courses': level_300_courses,
    }

    return render(request, 'reviews/course_list.html', context)





def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    reviews = Review.objects.filter(course=course)

    if request.method == "POST" and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
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

    return render(request, 'reviews/course_detail.html', {'course': course, 'reviews': reviews, 'form': form})
