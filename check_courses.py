import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CourseReviews1.settings')
django.setup()

# Import models
from reviews.models import Course

# Get and display LUC courses
luc_courses = Course.objects.filter(university_college='luc')
print(f'Total LUC courses: {luc_courses.count()}')
print('\nSample LUC courses:')
for course in luc_courses[:10]:
    print(f'- {course.name}')
    print(f'  Code: {course.code}')
    print(f'  Level: {course.level}')
    if course.description:
        print(f'  Description: {course.description[:100]}...' if len(course.description) > 100 
              else f'  Description: {course.description}')
    print() 