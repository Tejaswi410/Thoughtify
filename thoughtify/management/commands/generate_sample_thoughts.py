from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from thoughtify.models import Thought, EmotionTag
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generates sample thoughts for each emotion tag'

    def handle(self, *args, **kwargs):
        # Sample thought templates
        thought_templates = [
            # Happy thoughts
            "Today was an amazing day because {}!",
            "I'm so happy that {}!",
            "Can't stop smiling because {}",
            "Just achieved {} and feeling great!",
            "Wonderful moment when {}",
            
            # Sad thoughts
            "Feeling down because {}",
            "Missing {} today",
            "Wish I could {}",
            "Hard times when {}",
            "Sometimes {} makes me sad",
            
            # Excited thoughts
            "Can't wait for {}!",
            "So thrilled about {}!",
            "Getting ready for {}!",
            "Amazing news: {}!",
            "Just found out about {}!",
            
            # Anxious thoughts
            "Worried about {}",
            "Not sure how to handle {}",
            "Feeling nervous about {}",
            "What if {}?",
            "Overthinking about {}",
            
            # Grateful thoughts
            "So thankful for {}",
            "Blessed to have {}",
            "Appreciating {} today",
            "Grateful moment: {}",
            "Thank you universe for {}",
            
            # Confused thoughts
            "Can't figure out {}",
            "Trying to understand {}",
            "Not sure about {}",
            "Mixed feelings about {}",
            "Should I {}?",
            
            # Hopeful thoughts
            "Looking forward to {}",
            "Better days ahead because {}",
            "Believing in {}",
            "One day I'll {}",
            "Dreams of {}",
            
            # Tired thoughts
            "Long day of {}",
            "Need rest after {}",
            "Exhausted from {}",
            "Time to recharge after {}",
            "Taking a break from {}"
        ]

        # Sample thought completions for each emotion
        completions = {
            'Happy': [
                "spending time with family",
                "achieving my goals",
                "the beautiful weather",
                "getting good news",
                "meeting old friends",
                "learning something new",
                "helping someone",
                "receiving a surprise",
                "completing a project",
                "making someone smile"
            ],
            'Sad': [
                "the rainy weather",
                "a missed opportunity",
                "an old memory",
                "a difficult situation",
                "not meeting expectations",
                "saying goodbye",
                "a tough decision",
                "feeling alone",
                "past mistakes",
                "changes in life"
            ],
            'Excited': [
                "the upcoming vacation",
                "starting a new project",
                "meeting someone special",
                "trying something new",
                "weekend plans",
                "a surprise party",
                "learning a new skill",
                "future possibilities",
                "an upcoming event",
                "good opportunities"
            ],
            'Anxious': [
                "upcoming deadlines",
                "important decisions",
                "future uncertainties",
                "challenging tasks",
                "new responsibilities",
                "unexpected changes",
                "meeting new people",
                "performance pressure",
                "time management",
                "life changes"
            ],
            'Grateful': [
                "supportive friends",
                "good health",
                "life lessons",
                "new opportunities",
                "simple pleasures",
                "family support",
                "peaceful moments",
                "daily blessings",
                "kind gestures",
                "life experiences"
            ],
            'Confused': [
                "life choices",
                "complex situations",
                "mixed signals",
                "difficult decisions",
                "unexpected events",
                "relationship dynamics",
                "career paths",
                "future plans",
                "others' behavior",
                "personal feelings"
            ],
            'Hopeful': [
                "new beginnings",
                "future opportunities",
                "positive changes",
                "personal growth",
                "achieving dreams",
                "making progress",
                "better tomorrow",
                "new possibilities",
                "good outcomes",
                "learning experiences"
            ],
            'Tired': [
                "a busy workday",
                "intense workout",
                "continuous meetings",
                "studying hard",
                "helping others",
                "problem solving",
                "multitasking",
                "daily responsibilities",
                "challenging tasks",
                "mental exercises"
            ]
        }

        # Get or create a user for sample thoughts
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            self.stdout.write(self.style.ERROR('No superuser found. Please create one first.'))
            return

        # Get all emotion tags
        emotion_tags = EmotionTag.objects.all()
        
        thoughts_created = 0
        
        # Generate thoughts for each emotion tag
        for emotion_tag in emotion_tags:
            emotion_name = emotion_tag.name
            if emotion_name not in completions:
                continue
                
            # Generate 10 thoughts for each emotion
            for i in range(10):
                template = random.choice(thought_templates)
                completion = random.choice(completions[emotion_name])
                content = template.format(completion)
                
                # Create thought with a random timestamp within the last week
                random_days = random.randint(0, 7)
                random_hours = random.randint(0, 23)
                random_minutes = random.randint(0, 59)
                timestamp = timezone.now() - timedelta(
                    days=random_days,
                    hours=random_hours,
                    minutes=random_minutes
                )
                
                thought = Thought.objects.create(
                    author=user,
                    content=content,
                    emotion_tag=emotion_tag,
                    sentiment='positive' if emotion_name in ['Happy', 'Excited', 'Grateful', 'Hopeful']
                            else 'negative' if emotion_name in ['Sad', 'Anxious', 'Tired']
                            else 'neutral',
                    is_public=True,
                    created_at=timestamp
                )
                thoughts_created += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Created thought for emotion {emotion_name}: {content[:50]}...'
                ))

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {thoughts_created} sample thoughts!'
        )) 