from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text', 'teacher_name', 'teacher_quality']
        widgets = {
            'rating': forms.NumberInput(attrs={'placeholder': 'Enter rating (1.0-5.0)'}),
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your thoughts'}),
            'teacher_name': forms.TextInput(attrs={'placeholder': 'Teacher\'s name (optional)'}),
            'teacher_quality': forms.NumberInput(attrs={'placeholder': 'Teacher quality (1-5)'}),
        }
        help_texts = {
            'rating': 'Enter a rating between 1.0 and 5.0',
            'text': 'Share your detailed feedback about the course',
            'teacher_name': '(Optional) Enter the teacher\'s name',
            'teacher_quality': '(Optional) Rate the teacher\'s quality on a scale of 1 to 5',
        }
