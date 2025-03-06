import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CourseReviews1.settings')
django.setup()

exclude_models = ['auth.permission', 'contenttypes']

print("Starting data dump...")

with open('datadump_utf8.json', 'w', encoding='utf-8') as file:
    call_command('dumpdata', exclude=exclude_models, stdout=file)

print("Data dump completed.")
