"""
URL configuration for CourseReviews1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from CourseReviews1 import views as core_views
from django.conf import settings
from django.conf.urls.static import static
import users.views as user_views
from django.views.generic import RedirectView
from django.conf.urls import handler404

# Import custom view for 404
from .views import custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:university_college>/users/', include('users.urls')),
    path('<str:university_college>/courses/', include('reviews.urls')),
    path('<str:university_college>/feedback/', include('feedback.urls')),
    path('<str:university_college>/forum/', include('forum.urls')),
    path('', core_views.homepage, name='homepage'),
    
    # Non-university specific routes for login and registration
    path('users/login/', user_views.college_selection_login, name='college_selection_login'),
    path('users/register/', user_views.college_selection_register, name='college_selection_register'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = 'CourseReviews1.views.custom_404_view'
