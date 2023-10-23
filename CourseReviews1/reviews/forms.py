from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }
        help_texts = {
            'rating': 'Please enter a rating between 1.0 and 5.0.',
        }
