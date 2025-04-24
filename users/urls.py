from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

app_name = 'users'

# The university_college parameter is included in the URL patterns
# as it's captured by the parent URLs in CourseReviews1/urls.py

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
] 