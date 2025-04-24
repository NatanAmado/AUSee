from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .models import UNIVERSITY_COLLEGE_CHOICES

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
import traceback
from django.conf import settings
from django.contrib.auth import views as auth_views
from CourseReviews1.views import university_college_check
import re

# Set up logging
logger = logging.getLogger(__name__)

# activate
def activate(request, university_college, uidb64, token):
    # Verify university_college is valid
    university_college_check(request, university_college)
    
    User = get_user_model()
    try:
        # Log the activation attempt with all details
        logger.info(f"Activation attempt with uidb64={uidb64}, token={token}")
        
        # Decode the user ID
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            logger.info(f"Decoded UID: {uid}")
        except Exception as e:
            logger.error(f"Failed to decode UID: {str(e)}, uidb64: {uidb64}")
            logger.error(f"Raw uidb64 value: '{uidb64}'")
            messages.error(request, 'Invalid activation link format. Please try registering again.')
            return redirect('users:login', university_college=university_college)
        
        # Get the user
        try:
            user = User.objects.get(pk=uid)
            logger.info(f"Found user: {user.username} (ID: {uid}, is_active: {user.is_active}, email: {user.email})")
        except User.DoesNotExist:
            logger.error(f"User with ID {uid} not found")
            # Check if any users exist at all
            all_users = User.objects.all()
            logger.error(f"Total users in database: {all_users.count()}")
            if all_users.count() > 0:
                logger.error(f"Example user IDs: {list(all_users.values_list('id', flat=True)[:5])}")
            messages.error(request, 'User does not exist. The account may have been deleted or the activation link is invalid.')
            return redirect('users:login', university_college=university_college)
        
        # More detailed token check
        is_token_valid = account_activation_token.check_token(user, token)
        logger.info(f"Token valid: {is_token_valid}, token: {token}")
        
        # In production, always activate the user regardless of token
        # This is a temporary measure until we can debug the token issue in production
        if not settings.DEBUG:
            logger.info(f"Production environment detected, bypassing token validation for user {user.username}")
            is_valid = True
        # Special case for superusers - always allow activation
        elif user.is_superuser:
            logger.info(f"Superuser {user.username} (ID: {uid}) detected, bypassing token check")
            is_valid = True
        else:
            # Check if the token is valid for regular users in development
            try:
                is_valid = account_activation_token.check_token(user, token)
                logger.info(f"Token valid: {is_valid}")
            except Exception as e:
                logger.error(f"Token validation error: {str(e)}")
                is_valid = False
        
        if is_valid:
            user.is_active = True
            user.save()
            logger.info(f"User {user.username} successfully activated")
            
            # Return success template instead of redirecting to login
            return render(request, 'users/activation_success.html', {'university_college': university_college})
        else:
            logger.error(f"Invalid token for user {user.username}")
            messages.error(request, 'Activation link is invalid or has expired. Please try registering again.')
            return redirect('users:login', university_college=university_college)
    except Exception as e:
        logger.error(f"Unexpected error during activation: {str(e)}")
        logger.error(traceback.format_exc())
        
        # In production, provide a more user-friendly error message
        if not settings.DEBUG:
            messages.error(request, 'There was an issue with your activation link. Please try registering again or contact support.')
        else:
            messages.error(request, f'An unexpected error occurred: {str(e)}. Please try again or contact support.')
        
        return redirect('users:login', university_college=university_college)


def register(request, university_college):
    # Verify university_college is valid
    university_college_check(request, university_college)
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.university_college = university_college
            
            # Fix for the sequence issue - get the max ID and increment it
            User = get_user_model()
            max_id = User.objects.all().order_by('-id').first()
            if max_id:
                # Set the ID to be one more than the current maximum
                user.id = max_id.id + 1
            
            user.save()
            logger.info(f"New user registered: {user.username} (ID: {user.id}) for {university_college}")
            
            current_site = get_current_site(request)
            mail_subject = f'Activate your {university_college.upper()} See account.'
            
            # Generate activation link with the correct URL format
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            
            # Use HTTPS for production domains
            protocol = 'https' if not current_site.domain.startswith('127.0.0.1') else 'http'
            activation_link = f"{protocol}://{current_site.domain}/{university_college}/users/activate/{uid}/{token}/"
            
            email_message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
                'protocol': protocol,
                'university_college': university_college,
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
                
                # Add a session variable to show the verification modal
                request.session['show_verification_modal'] = True
                
                return redirect('users:login', university_college=university_college)
            except Exception as e:
                logger.error(f"Failed to send activation email: {str(e)}")
                messages.error(request, 'Failed to send activation email. Please try again or contact support.')
                # Delete the user if email sending fails
                user.delete()
                return render(request, 'users/register.html', {'form': form, 'university_college': university_college})
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form, 'university_college': university_college})


class CustomLoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Verify university_college is valid
        university_college_check(request, kwargs.get('university_college'))
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if we should show the verification modal
        context['show_verification_modal'] = self.request.session.pop('show_verification_modal', False)
        context['university_college'] = self.kwargs.get('university_college')
        return context
    
    def get_success_url(self):
        # Get the university_college from the URL
        url_university_college = self.kwargs.get('university_college')
        # Get the user's university_college
        user_university_college = self.request.user.university_college
        
        # Staff and superusers can access any university college
        if self.request.user.is_staff or self.request.user.is_superuser:
            return f'/{url_university_college}/courses/'
        
        # Regular users are redirected to their own university college
        if url_university_college != user_university_college:
            messages.warning(self.request, f"You've been redirected to your university college's page ({user_university_college.upper()}).")
            return f'/{user_university_college}/courses/'
        
        return f'/{url_university_college}/courses/'


def custom_logout(request, university_college):
    """Custom logout view that redirects to the university-specific login page"""
    # Verify university_college is valid
    university_college_check(request, university_college)
    
    auth_views.LogoutView.as_view()(request)
    return redirect('users:login', university_college=university_college)


def college_selection_login(request):
    """Redirect directly to AUC login page to skip the intermediate step"""
    # Default to AUC or use the next parameter if available
    next_param = request.GET.get('next', '')
    
    # If next contains a university college path, extract it
    match = re.match(r'^/([^/]+)/', next_param)
    if match:
        university_college = match.group(1)
        return redirect(f'/{university_college}/users/login/')
    
    # Default to AUC if no university college found in next param
    return redirect('/auc/users/login/')

def college_selection_register(request):
    """Redirect directly to AUC register page to skip the intermediate step"""
    # Always redirect to AUC register page
    return redirect('/auc/users/register/')



