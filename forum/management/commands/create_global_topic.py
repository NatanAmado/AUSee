from django.core.management.base import BaseCommand
from django.db.models import Q
from forum.models import Topic
from users.models import CustomUser, UNIVERSITY_COLLEGE_CHOICES

class Command(BaseCommand):
    help = 'Creates a global discussion topic accessible to students from all university colleges'

    def handle(self, *args, **options):
        # Check if a global topic already exists
        global_topic = Topic.objects.filter(is_global=True).first()
        
        if global_topic:
            self.stdout.write(self.style.SUCCESS(f'Global topic "{global_topic.name}" already exists!'))
            return
        
        # Find a superuser to be the creator of the topic
        superuser = CustomUser.objects.filter(is_superuser=True).first()
        
        if not superuser:
            self.stdout.write(self.style.ERROR('No superuser found! Please create a superuser first.'))
            return
        
        # Create the global topic
        global_topic = Topic.objects.create(
            name="Campus Connect - Inter-University Discussion",
            description="Welcome to Campus Connect! This is a global forum where students from all university colleges can interact. Feel free to discuss topics that are relevant across all campuses, share experiences, and connect with students from other university colleges.",
            created_by=superuser,
            university_college='auc',  # Default college, but will be shown to all
            is_global=True
        )
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created global topic "{global_topic.name}"')) 