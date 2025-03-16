from django import forms
from .models import Review, Course, ReviewReply, ReviewReport

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

class ReviewReplyForm(forms.ModelForm):
    is_anonymous = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = ReviewReply
        fields = ['text', 'is_anonymous']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your reply here...', 'class': 'form-control'}),
        }
        labels = {
            'text': 'Reply:',
            'is_anonymous': 'Post anonymously',
        }

class ReviewReportForm(forms.ModelForm):
    class Meta:
        model = ReviewReport
        fields = ['reason', 'additional_info']
        widgets = {
            'additional_info': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Provide additional details about your report...', 'class': 'form-control'}),
            'reason': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'reason': 'Reason for reporting:',
            'additional_info': 'Additional information (optional):',
        }

        


