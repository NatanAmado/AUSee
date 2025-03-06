# feedback/forms.py
from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback']

        labels = {
            'feedback': 'Your Feedback:',
        }

        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Let us know how we can improve... '}),
        }
