# Generated by Django 4.2.7 on 2025-03-04 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0009_remove_review_downvotes_remove_review_upvotes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='CourseReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='reviews.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('course', 'user')},
            },
        ),
    ]
