# Generated by Django 4.2.7 on 2025-03-16 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0014_review_archived_reviewreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewreply',
            name='is_anonymous',
            field=models.BooleanField(default=True),
        ),
    ]
