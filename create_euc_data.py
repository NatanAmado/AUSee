import pandas as pd
import os

# Create a data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Create EUC sample data based on the image provided and extended with more courses
data = [
    {
        'Name': 'Economics 101',
        'Level': 100,
        'Course Code': 'ECO101',
        'Cluster/Department': 'Academic Core Courses (ACC)',
    },
    {
        'Name': 'Microeconomics',
        'Level': 200,
        'Course Code': 'ECO201',
        'Cluster/Department': 'Economics (ECO)',
    },
    {
        'Name': 'Macroeconomics',
        'Level': 200,
        'Course Code': 'ECO202',
        'Cluster/Department': 'Economics (ECO)',
    },
    {
        'Name': 'International Economics',
        'Level': 300,
        'Course Code': 'ECO301',
        'Cluster/Department': 'Economics (ECO)',
    },
    {
        'Name': 'Introduction to Life Sciences',
        'Level': 100,
        'Course Code': 'LSC101',
        'Cluster/Department': 'Life Sciences (LSC)',
    },
    {
        'Name': 'Cell Biology',
        'Level': 200,
        'Course Code': 'LSC201',
        'Cluster/Department': 'Life Sciences (LSC)',
    },
    {
        'Name': 'Genetics',
        'Level': 300,
        'Course Code': 'LSC301',
        'Cluster/Department': 'Life Sciences (LSC)',
    },
    {
        'Name': 'Introduction to Humanities',
        'Level': 100,
        'Course Code': 'HUM101',
        'Cluster/Department': 'Humanities (HUM)',
    },
    {
        'Name': 'Philosophy',
        'Level': 200,
        'Course Code': 'HUM201',
        'Cluster/Department': 'Humanities (HUM)',
    },
    {
        'Name': 'Literature',
        'Level': 200,
        'Course Code': 'HUM202',
        'Cluster/Department': 'Humanities (HUM)',
    },
    {
        'Name': 'Introduction to Social Sciences',
        'Level': 100,
        'Course Code': 'SSC101',
        'Cluster/Department': 'Social Sciences (SSC)',
    },
    {
        'Name': 'Psychology',
        'Level': 200,
        'Course Code': 'SSC201',
        'Cluster/Department': 'Social Sciences (SSC)',
    },
    {
        'Name': 'Sociology',
        'Level': 200,
        'Course Code': 'SSC202',
        'Cluster/Department': 'Social Sciences (SSC)',
    },
    {
        'Name': 'Political Science',
        'Level': 300,
        'Course Code': 'SSC301',
        'Cluster/Department': 'Social Sciences (SSC)',
    },
]

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel file
excel_path = 'data/euc_courses.xlsx'
df.to_excel(excel_path, index=False)

print(f"Created sample EUC courses Excel file at {excel_path}")
print("Sample data from the file:")
print(df.head())
print("\nTotal courses: ", len(df))
print("\nMajors/Departments:")
for dept in sorted(df['Cluster/Department'].unique()):
    print(f"- {dept}")

print("\nYou can now import this file using:")
print("python3 manage.py import_excel_courses data/euc_courses.xlsx --university_college=euc") 