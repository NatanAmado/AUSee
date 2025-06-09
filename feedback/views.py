# feedback/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import FeedbackForm
from .models import Feedback
from CourseReviews1.views import university_college_check

@login_required
def feedback(request, university_college):
    # Verify university_college is valid
    university_college_check(request, university_college)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.name = request.user
            feedback.university_college = university_college
            feedback.save()
            return render(request, 'feedback/feedbackform_success.html', {'university_college': university_college})
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedbackform.html', {'form': form, 'university_college': university_college})


@login_required
def about(request, university_college):
    # Verify university_college is valid
    university_college_check(request, university_college)
    
    return render(request, 'feedback/about.html', {'university_college': university_college})

def form(request, university_college):
    # Verify university_college is valid
    university_college_check(request, university_college)
    
    return render(request, 'feedback/googleform.html', {'university_college': university_college})

@login_required
def feedback_list(request, university_college):
    # Verify university_college is valid
    university_college_check(request, university_college)
    
    feedbacks = Feedback.objects.filter(university_college=university_college).order_by('-created_at')
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks, 'university_college': university_college})

def feedback_view(request, university_college):
    # Verify university_college is valid
    university_college_check(request, university_college)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            
            # Prepare email content
            subject = 'New Anonymous Feedback Received'
            message = f"""
            New feedback received:
            
            Feedback: {feedback.feedback}
            
            Email (if provided): {feedback.email or 'Not provided'}
            
            Time: {feedback.created_at}
            """
            
            # Send email to both addresses
            recipient_list = ['auseecourses@gmail.com', 'contact@ausee.courses']
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False,
            )
            
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback:feedback', university_college=university_college)
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback/feedback_form.html', {
        'form': form,
        'university_college': university_college
    })