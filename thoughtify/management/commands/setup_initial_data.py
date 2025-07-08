from django.core.management.base import BaseCommand
from thoughtify.models import EmotionTag

class Command(BaseCommand):
    help = 'Sets up initial data for the Thoughtify app'

    def handle(self, *args, **kwargs):
        # Create emotion tags
        emotions = [
            'Happy', 'Sad', 'Excited', 'Anxious',
            'Grateful', 'Confused', 'Hopeful', 'Tired'
        ]
        
        created_count = 0
        for emotion in emotions:
            tag, created = EmotionTag.objects.get_or_create(name=emotion)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created emotion tag: {emotion}'))
        
        if created_count == 0:
            self.stdout.write(self.style.WARNING('All emotion tags already exist'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} emotion tags')) 