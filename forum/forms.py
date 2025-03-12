from django import forms
from .models import Topic, Post, Comment, TopicReport

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class TopicDescriptionForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'form-control',
                'placeholder': 'Enter a detailed description of this topic...'
            }),
        }
        labels = {
            'description': 'Topic Description'
        }
        help_texts = {
            'description': 'Provide a clear description of what this topic is about.'
        }

class TopicReportForm(forms.ModelForm):
    class Meta:
        model = TopicReport
        fields = ['reason', 'additional_info']
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-select'}),
            'additional_info': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Please provide additional details about your report...'
            }),
        }
        labels = {
            'additional_info': 'Additional Information'
        }

class PostForm(forms.ModelForm):
    is_anonymous = forms.BooleanField(
        required=False, 
        label="Post anonymously",
        help_text="If checked, your username will not be displayed with this post."
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'topic', 'is_anonymous']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
            'topic': forms.Select(attrs={'class': 'form-select'}),
        }

class CommentForm(forms.ModelForm):
    is_anonymous = forms.BooleanField(
        required=False, 
        label="Comment anonymously",
        help_text="If checked, your username will not be displayed with this comment."
    )
    
    class Meta:
        model = Comment
        fields = ['content', 'is_anonymous']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        } 