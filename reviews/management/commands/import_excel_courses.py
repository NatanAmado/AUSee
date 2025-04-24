from django.core.management.base import BaseCommand
import pandas as pd
from reviews.models import Course
import os

class Command(BaseCommand):
    help = 'Imports courses from a given Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='The path to the Excel file')
        parser.add_argument('--university_college', type=str, default='luc', 
                           help='University college code (default: luc)')

    def handle(self, *args, **kwargs):
        excel_file_path = kwargs['excel_file']
        university_college = kwargs['university_college'].lower()
        
        if not os.path.exists(excel_file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {excel_file_path}'))
            return
        
        try:
            # Read the Excel file
            df = pd.read_excel(excel_file_path)
            
            # Normalize column names (lowercase and strip spaces)
            df.columns = [col.lower().strip() for col in df.columns]
            
            # Map common column names to expected names
            column_mappings = {
                'name': 'name',
                'title': 'name',
                'course': 'name',
                'course name': 'name',
                'course title': 'name',
                'level': 'level',
                'course level': 'level',
                'code': 'code',
                'course code': 'code',
                'major': 'major',
                'department': 'major',
                'cluster/department': 'major',
                'cluster': 'major',
                'description': 'description',
                'course description': 'description'
            }
            
            # Rename columns based on mappings
            for col in df.columns:
                if col in column_mappings:
                    df = df.rename(columns={col: column_mappings[col]})
            
            # Check if required column exists
            if 'name' not in df.columns:
                self.stdout.write(self.style.ERROR('Required column not found: name/title/course'))
                return
            
            courses_created = 0
            courses_skipped = 0
            majors_found = set()
            
            # Process each row in the Excel file
            for _, row in df.iterrows():
                course_name = str(row.get('name', '')).strip()
                
                # Skip rows with empty course names
                if not course_name or course_name.lower() == 'nan':
                    continue
                
                # Get other fields if they exist
                description = str(row.get('description', '')).strip() if 'description' in row else ''
                if description.lower() == 'nan':
                    description = ''
                    
                # Get major/department information
                major = str(row.get('major', '')).strip() if 'major' in row else ''
                if major.lower() == 'nan':
                    major = ''
                
                # Store majors for reporting
                if major:
                    majors_found.add(major)
                
                # Get course code
                code = str(row.get('code', '')).strip() if 'code' in row else ''
                if code.lower() == 'nan':
                    code = major if major else '--'
                
                # Determine course level (default to 100)
                level = 100
                if 'level' in row:
                    try:
                        level_value = row['level']
                        # Handle level values that might be strings
                        if isinstance(level_value, str):
                            # Try to extract numeric value
                            import re
                            level_match = re.search(r'\d+', level_value)
                            if level_match:
                                raw_level = int(level_match.group())
                            else:
                                raw_level = 100
                        else:
                            raw_level = int(level_value)
                            
                        # Map to the closest level in LEVEL_CHOICES
                        if raw_level >= 300:
                            level = 300
                        elif raw_level >= 200:
                            level = 200
                        else:
                            level = 100
                    except (ValueError, TypeError):
                        # If level can't be converted to int, use default
                        self.stdout.write(f'Invalid level value for {course_name}: {row.get("level")}, using default (100)')
                
                # Check if course already exists
                if Course.objects.filter(name=course_name, university_college=university_college).exists():
                    self.stdout.write(f'Course already exists: {course_name}')
                    courses_skipped += 1
                    continue
                
                # Create the course
                Course.objects.create(
                    name=course_name,
                    code=code,
                    description=description,
                    level=level,
                    university_college=university_college
                )
                courses_created += 1
            
            self.stdout.write(self.style.SUCCESS(
                f'Successfully imported {courses_created} courses from the Excel file'
                f' ({courses_skipped} skipped as duplicates)'
            ))
            
            if majors_found:
                self.stdout.write("Majors/departments found for filtering:")
                for major in sorted(majors_found):
                    self.stdout.write(f"- {major}")
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing courses: {str(e)}')) 