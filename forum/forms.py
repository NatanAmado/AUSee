from django import forms
from .models import Topic, Post, Comment

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
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