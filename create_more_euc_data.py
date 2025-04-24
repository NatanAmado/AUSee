import pandas as pd
import os
import random

# Create a data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Define various departments and their codes
departments = [
    ('Economics', 'ECO'),
    ('Life Sciences', 'LSC'),
    ('Humanities', 'HUM'),
    ('Social Sciences', 'SSC'),
    ('Mathematics', 'MAT'),
    ('Computer Science', 'CSC'),
    ('Physics', 'PHY'),
    ('Chemistry', 'CHM'),
    ('Geography', 'GEO'),
    ('History', 'HIS'),
    ('Philosophy', 'PHI'),
    ('International Relations', 'IRL'),
    ('Academic Core Courses', 'ACC'),
    ('Arts', 'ART'),
    ('Languages', 'LAN'),
    ('Political Science', 'POL'),
    ('Psychology', 'PSY'),
    ('Anthropology', 'ANT'),
    ('Business', 'BUS'),
    ('Communication', 'COM')
]

# Course names for each department
course_names = {
    'ECO': [
        'Introduction to Economics', 'Microeconomics', 'Macroeconomics', 'International Economics',
        'Development Economics', 'Econometrics', 'Behavioral Economics', 'Economic History',
        'Financial Economics', 'Public Economics', 'Labor Economics', 'Game Theory',
        'Money and Banking', 'Economics of Climate Change'
    ],
    'LSC': [
        'Introduction to Life Sciences', 'Cell Biology', 'Genetics', 'Molecular Biology',
        'Ecology', 'Physiology', 'Biochemistry', 'Neuroscience', 'Immunology',
        'Evolutionary Biology', 'Microbiology', 'Developmental Biology'
    ],
    'HUM': [
        'Introduction to Humanities', 'Philosophy', 'Literature', 'Cultural Studies',
        'Art History', 'Linguistics', 'Religious Studies', 'Classical Studies',
        'Media Studies', 'Film Studies', 'Modern Languages', 'Critical Theory'
    ],
    'SSC': [
        'Introduction to Social Sciences', 'Psychology', 'Sociology', 'Political Science',
        'Anthropology', 'Economics', 'Geography', 'International Relations',
        'Development Studies', 'Gender Studies', 'Urban Studies', 'Social Policy'
    ],
    'MAT': [
        'Calculus I', 'Calculus II', 'Linear Algebra', 'Discrete Mathematics',
        'Probability Theory', 'Statistics', 'Differential Equations', 'Numerical Analysis',
        'Mathematical Modeling', 'Abstract Algebra', 'Real Analysis', 'Complex Analysis'
    ],
    'CSC': [
        'Introduction to Programming', 'Data Structures and Algorithms', 'Computer Architecture',
        'Operating Systems', 'Database Systems', 'Computer Networks', 'Artificial Intelligence',
        'Machine Learning', 'Software Engineering', 'Web Development', 
        'Computer Graphics', 'Theoretical Computer Science'
    ],
    'PHY': [
        'Classical Mechanics', 'Electromagnetism', 'Quantum Mechanics', 'Thermodynamics',
        'Optics', 'Nuclear Physics', 'Particle Physics', 'Astrophysics',
        'Solid State Physics', 'Statistical Mechanics', 'Relativity', 'Experimental Physics'
    ],
    'CHM': [
        'General Chemistry', 'Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry',
        'Analytical Chemistry', 'Biochemistry', 'Chemical Kinetics', 'Environmental Chemistry',
        'Medicinal Chemistry', 'Polymer Chemistry', 'Spectroscopy', 'Computational Chemistry'
    ],
    'GEO': [
        'Physical Geography', 'Human Geography', 'Economic Geography', 'Political Geography',
        'Urban Geography', 'Environmental Geography', 'Geographical Information Systems',
        'Climate Change Studies', 'Geomorphology', 'Biogeography', 
        'Regional Development', 'Geographic Research Methods'
    ],
    'HIS': [
        'World History', 'European History', 'Asian History', 'American History',
        'History of Science', 'Economic History', 'Social History', 'Cultural History',
        'Medieval History', 'Modern History', 'Diplomatic History', 'Military History'
    ],
    'PHI': [
        'Ethics', 'Logic', 'Metaphysics', 'Epistemology', 'Philosophy of Mind',
        'Political Philosophy', 'Aesthetics', 'Existentialism', 'Ancient Philosophy',
        'Modern Philosophy', 'Continental Philosophy', 'Analytic Philosophy'
    ],
    'IRL': [
        'International Relations Theory', 'Global Governance', 'Security Studies',
        'Peace and Conflict Studies', 'International Organizations', 'Foreign Policy Analysis',
        'International Law', 'International Political Economy', 'Human Rights',
        'Global Environmental Politics', 'Regional Integration', 'Diplomacy'
    ],
    'ACC': [
        'Academic Writing', 'Research Methods', 'Critical Thinking', 'Data Analysis',
        'Presentation Skills', 'Digital Literacy', 'Ethics and Society', 'Scientific Reasoning',
        'Intercultural Communication', 'Academic English', 'Mathematics for Academic Purposes',
        'Information Literacy'
    ],
    'ART': [
        'Visual Arts', 'Performing Arts', 'Music Theory', 'Art History', 'Studio Art',
        'Digital Media', 'Film Studies', 'Photography', 'Sculpture', 'Painting',
        'Graphic Design', 'Theater Studies'
    ],
    'LAN': [
        'Spanish', 'French', 'German', 'Italian', 'Mandarin Chinese', 'Japanese',
        'Russian', 'Arabic', 'Latin', 'Ancient Greek', 'Dutch', 'Portuguese'
    ],
    'POL': [
        'Political Theory', 'Comparative Politics', 'Political Institutions', 'Public Policy',
        'Electoral Systems', 'Democracy Studies', 'Political Behavior', 'Political Economy',
        'European Politics', 'Identity Politics', 'Global Politics', 'Policy Analysis'
    ],
    'PSY': [
        'Cognitive Psychology', 'Social Psychology', 'Developmental Psychology', 'Clinical Psychology',
        'Personality Psychology', 'Behavioral Psychology', 'Abnormal Psychology', 'Neuropsychology',
        'Positive Psychology', 'Health Psychology', 'Industrial-Organizational Psychology', 'Educational Psychology'
    ],
    'ANT': [
        'Cultural Anthropology', 'Social Anthropology', 'Biological Anthropology', 'Archaeological Anthropology',
        'Linguistic Anthropology', 'Medical Anthropology', 'Economic Anthropology', 'Political Anthropology',
        'Urban Anthropology', 'Digital Anthropology', 'Visual Anthropology', 'Environmental Anthropology'
    ],
    'BUS': [
        'Management', 'Marketing', 'Finance', 'Accounting', 'Human Resource Management',
        'Operations Management', 'Business Strategy', 'Entrepreneurship', 'Corporate Social Responsibility',
        'Business Ethics', 'International Business', 'Business Law'
    ],
    'COM': [
        'Media Studies', 'Communication Theory', 'Digital Media', 'Journalism', 'Public Relations',
        'Advertising', 'Intercultural Communication', 'Mass Communication', 'Political Communication',
        'Health Communication', 'Organizational Communication', 'Visual Communication'
    ]
}

# Generate courses data
data = []

for dept_name, dept_code in departments:
    # Get course names for this department
    names = course_names.get(dept_code, [f'{dept_name} Course'])
    
    # Generate courses for each level
    for level in [100, 200, 300]:
        # Number of courses for this department and level
        num_courses = random.randint(3, 6)
        
        # Select random course names
        selected_names = random.sample(names, min(num_courses, len(names)))
        
        for i, name in enumerate(selected_names):
            # Create course code
            course_code = f"{dept_code}{level}{i+1:02d}"
            
            # Create description
            description = f"This course introduces students to {name.lower()} concepts in the field of {dept_name.lower()}. "
            description += f"Students will explore key theories, methodologies, and applications relevant to {dept_name.lower()} studies. "
            description += f"The course includes lectures, discussions, and practical assignments."
            
            # Add to data
            data.append({
                'Name': name,
                'Level': level,
                'Course Code': course_code,
                'Cluster/Department': f'{dept_name} ({dept_code})',
                'Description': description
            })

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel file
excel_path = 'data/euc_extended_courses.xlsx'
df.to_excel(excel_path, index=False)

print(f"Created extended EUC courses Excel file at {excel_path}")
print(f"Total courses: {len(df)}")
print("\nCourses by department:")
dept_counts = df['Cluster/Department'].value_counts()
for dept, count in dept_counts.items():
    print(f"- {dept}: {count} courses")

print("\nYou can now import this file using:")
print("python3 manage.py import_excel_courses data/euc_extended_courses.xlsx --university_college=euc") 