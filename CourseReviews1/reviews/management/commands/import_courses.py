from django.core.management.base import BaseCommand
import csv
from reviews.models import Course

class Command(BaseCommand):
    help = 'Imports courses from a given CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Course.objects.create(
                    name=row['coursename'],
                    code="--",
                    level=row['courselevel']
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported courses from the CSV file'))
