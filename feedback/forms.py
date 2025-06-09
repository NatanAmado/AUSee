# feedback/forms.py
from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback', 'email']

        labels = {
            'feedback': 'Your Feedback:',
            'email': 'Your Email (optional):',
        }

        widgets = {
            'feedback': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Please share your thoughts, suggestions, or concerns...',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email if you want us to respond',
                'class': 'form-control'
            }),
        }
