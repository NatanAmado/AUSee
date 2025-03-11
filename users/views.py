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

# activate
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token): 
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully!')
        return render(request, 'users/activation_success.html')
    else:
        messages.error(request, 'Activation link is invalid or has expired!')
        return redirect('users:login')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            
            # Fix for the sequence issue - get the max ID and increment it
            User = get_user_model()
            max_id = User.objects.all().order_by('-id').first()
            if max_id:
                # Set the ID to be one more than the current maximum
                user.id = max_id.id + 1
            
            user.save()
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your AUSee account.'
            
            # Generate activation link with the correct URL format
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = f"http://{current_site.domain}/users/activate/{uid}/{token}/"
            
            # Store activation link in session for display on login page
            request.session['activation_link'] = activation_link
            
            email_message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token, 
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, email_message, to=[to_email]
            )
            email.content_subtype = "html"  # Set the content type as HTML
            email.send()
            messages.success(request, f'Account created successfully! Please check your email ({to_email}) to activate your account. Check your spam folder if you don\'t see it.')
            login(request, user)
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})



