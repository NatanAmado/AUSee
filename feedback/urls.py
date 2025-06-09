from django.urls import path
from . import views

app_name = 'feedback'

# The university_college parameter is captured from the parent URL pattern
# in CourseReviews1/urls.py and passed to each view
urlpatterns = [
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('form/', views.form, name='form'),
    path('list/', views.feedback_list, name='feedback_list'),
] 