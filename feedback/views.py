# feedback/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm
from .models import Feedback

@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.name = request.user
            feedback.save()
            return render(request, 'feedback/feedbackform_success.html')  # Redirect to a 'success' page after submitting.
    else:
        form = FeedbackForm()
    return render(request, 'feedback/feedbackform.html', {'form': form})



@login_required
def about(request):
    return render(request, 'feedback/about.html')

def form(request):
    return render(request, 'feedback/googleform.html')

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'feedback/feedback_list.html', {'feedbacks': feedbacks})