# Generated by Django 4.2.7 on 2024-01-11 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(default="Your email should be a student email'", max_length=254),
        ),
    ]
