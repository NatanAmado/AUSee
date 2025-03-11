from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView


app_name = 'feedback'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),
    path('form/', views.form, name='form'),
    

]