from django import forms
from .models import Review, Course

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text', 'teacher_name', 'teacher_quality']
        widgets = {
            
            'text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Share your thoughts about this course... '}),
            'teacher_name': forms.Textarea(attrs={'rows': 1}),

            
        }
        help_texts = {
            'rating': 'Enter a rating between 1.0 and 5.0',
            'teacher_name': '(Optional)',
            'teacher_quality': '(Optional)',
        }
        labels = {
            'text': 'Review:',
            'teacher_name': 'Teacher Name:',
            'teacher_quality': 'Teacher Quality:',
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'level', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Provide a description of the course...'}),
        }
        labels = {
            'name': 'Course Name:',
            'code': 'Course Code:',
            'level': 'Course Level:',
            'description': 'Description:',
        }

        


