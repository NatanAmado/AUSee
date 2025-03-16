from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import MAJOR_CHOICES
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    major = forms.ChoiceField(choices=MAJOR_CHOICES)
    email = forms.EmailField(
        label="Student Email",
        widget=forms.EmailInput(attrs={'placeholder': 'your.name@student.auc.nl'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'major', 'track')  # Add any other fields you want in the registration form
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'This will be fully anonymous...'}),
            'major': forms.TextInput(attrs={'placeholder': 'Enter major'}),
            'track': forms.TextInput(attrs={'placeholder': 'Enter track'}),
        }
        help_texts = {
            'uservame': "Only you are able to see this."
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@student.auc.nl'):
            raise ValidationError("Email must end with '@student.auc.nl'")
        return email