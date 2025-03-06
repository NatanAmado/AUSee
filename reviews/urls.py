from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('add/', views.add_course, name='add_course'),
    path('<int:course_id>/report/', views.report_course, name='report_course'),
    # ... other url patterns will go here later ...
]


