from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from thoughtify.models import UserProfile
import random
import string

class Command(BaseCommand):
    help = 'Creates UserProfile for users that don\'t have one'

    def generate_anonymous_code(self):
        """Generate a random 8-character anonymous code."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def handle(self, *args, **kwargs):
        users_without_profile = []
        profiles_created = 0

        # Get all users
        for user in User.objects.all():
            try:
                # Try to access the user's profile
                user.userprofile
            except User.userprofile.RelatedObjectDoesNotExist:
                users_without_profile.append(user)

        # Create profiles for users that don't have one
        for user in users_without_profile:
            # Generate a unique anonymous code
            while True:
                anonymous_code = self.generate_anonymous_code()
                if not UserProfile.objects.filter(anonymous_code=anonymous_code).exists():
                    break

            UserProfile.objects.create(
                user=user,
                anonymous_code=anonymous_code,
                bio=f"Sample bio for {user.username}"
            )
            profiles_created += 1
            self.stdout.write(
                self.style.SUCCESS(f'Created profile for user {user.username} with code {anonymous_code}')
            )

        if profiles_created == 0:
            self.stdout.write(self.style.SUCCESS('All users already have profiles!'))
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {profiles_created} user profiles!')
            ) 