from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import logging

# Set up logging
logger = logging.getLogger(__name__)

# activate
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        logger.info(f"Attempting to activate user with ID: {uid}")
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None
        logger.error(f"Error decoding user ID or finding user: {str(e)}")
    
    if user is not None and account_activation_token.check_token(user, token): 
        # Only activate if not already active
        if not user.is_active:
            user.is_active = True
            user.save()
            logger.info(f"User {user.username} (ID: {uid}) activated successfully")
            messages.success(request, 'Your account has been activated successfully! You can now log in.')
            return redirect('users:login')
        else:
            logger.info(f"User {user.username} (ID: {uid}) is already active")
            messages.info(request, 'Your account is already active. You can log in.')
            return redirect('users:login')
    else:
        if user is not None:
            logger.warning(f"Invalid token for user {user.username} (ID: {uid})")
        else:
            logger.warning(f"Activation attempt with invalid user ID: {uidb64}")
        
        messages.error(request, 'Activation link is invalid or has expired! Please register again or contact support.')
        return redirect('users:login')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            
            # Fix for the sequence issue - get the max ID and increment it
            User = get_user_model()
            max_id = User.objects.all().order_by('-id').first()
            if max_id:
                # Set the ID to be one more than the current maximum
                user.id = max_id.id + 1
            
            user.save()
            logger.info(f"New user registered: {user.username} (ID: {user.id})")
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your AUSee account.'
            
            # Generate activation link with the correct URL format
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            
            # Use HTTPS for production domains
            protocol = 'https' if not current_site.domain.startswith('127.0.0.1') else 'http'
            activation_link = f"{protocol}://{current_site.domain}/users/activate/{uid}/{token}/"
            
            email_message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
                'protocol': protocol,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, email_message, to=[to_email]
            )
            email.content_subtype = "html"  # Set the content type as HTML
            
            try:
                email.send()
                logger.info(f"Activation email sent to {to_email}")
                messages.success(request, f'Account created successfully! Please check your email ({to_email}) to activate your account. Check your spam folder if you don\'t see it.')
                
                return redirect('users:login')
            except Exception as e:
                logger.error(f"Failed to send activation email: {str(e)}")
                messages.error(request, 'Failed to send activation email. Please try again or contact support.')
                # Delete the user if email sending fails
                user.delete()
                return render(request, 'users/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})



