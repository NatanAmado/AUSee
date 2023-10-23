from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    # ... other url patterns will go here later ...
]


