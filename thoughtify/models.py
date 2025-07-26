from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
from django.core.validators import FileExtensionValidator

class EmotionTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

EMOJI_CHOICES = [
    ('🙂', 'Smiling'),
    ('😎', 'Cool'),
    ('🤓', 'Nerdy'),
    ('😂', 'Laughing'),
    ('🥳', 'Party'),
    ('😇', 'Innocent'),
    ('😈', 'Mischievous'),
    ('🤠', 'Cowboy'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    anonymous_code = models.CharField(max_length=4, unique=True)
    show_public_thoughts = models.BooleanField(default=True)
    last_daily_thought = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.anonymous_code

    @staticmethod
    def generate_anonymous_code(username):
        first_letter = username[0].upper()
        while True:
            random_number = random.randint(1, 999)
            code = f"{first_letter}{random_number:03d}"
            if not UserProfile.objects.filter(anonymous_code=code).exists():
                return code

    def can_post_daily_thought(self):
        if not self.last_daily_thought:
            return True
        return self.last_daily_thought < timezone.now().date()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thought = models.ForeignKey('Thought', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'thought')

    def __str__(self):
        return f"{self.user.username} likes {self.thought.id}"

class Thought(models.Model):
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]

    # Make author nullable initially to handle migration
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,  # Allow null temporarily for migration
        blank=True,  # Allow blank temporarily for migration
    )
    content = models.CharField(max_length=280)
    emotion_tag = models.ForeignKey(EmotionTag, on_delete=models.SET_NULL, null=True)
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, default='neutral')
    is_daily_thought = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]

    def __str__(self):
        if self.author and hasattr(self.author, 'userprofile'):
            return f"{self.author.userprofile.anonymous_code}: {self.content[:50]}..."
        return f"Anonymous: {self.content[:50]}..."

    @property
    def author_code(self):
        if self.author and hasattr(self.author, 'userprofile'):
            return self.author.userprofile.anonymous_code
        return 'Anonymous'

    @property
    def likes_count(self):
        return self.likes.count()

class DraftThought(models.Model):
    """Store thoughts from non-logged-in users temporarily"""
    content = models.CharField(max_length=280)
    emotion_tag = models.ForeignKey(EmotionTag, on_delete=models.SET_NULL, null=True)
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(default=timezone.now)

    def publish(self, user):
        """Convert draft to actual thought"""
        thought = Thought.objects.create(
            author=user,
            content=self.content,
            emotion_tag=self.emotion_tag
        )
        self.delete()
        return thought
