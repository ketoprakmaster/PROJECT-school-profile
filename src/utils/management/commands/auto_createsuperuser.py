import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from decouple import config


try:
    USERNAME: str = config("DJANGO_SUPERUSER_USERNAME", cast=str)
    EMAIL: str = config("DJANGO_SUPERUSER_EMAIL", cast=str)
    PASSWORD: str = config("DJANGO_SUPERUSER_PASSWORD", cast=str)
except Exception as e:
    print(f"Error loading superuser credentials from environment: {e}")
    # Setting an empty string as a default which will be caught later.
    USERNAME = ""
    EMAIL = ""
    PASSWORD = ""


class Command(BaseCommand):
    help = 'Automatically creates a superuser using environment variables if one does not exist.'

    def handle(self, *args, **options):
        User = get_user_model()
        
        if not all([USERNAME, EMAIL, PASSWORD]):
            raise CommandError(
                self.style.ERROR(
                    "Superuser creation failed: DJANGO_SUPERUSER_USERNAME, "
                    "DJANGO_SUPERUSER_EMAIL, and DJANGO_SUPERUSER_PASSWORD "
                    "must be set in your environment configuration."
                )
            )

        if User.objects.filter(username=USERNAME).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{USERNAME}" already exists. Skipping creation.')
            )
            return

        try:
            User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Successfully created superuser: "{USERNAME}"')
            )
        except Exception as e:
            raise CommandError(
                self.style.ERROR(
                    f'Superuser creation failed for "{USERNAME}". Error: {e}'
                )
            )


# pyright: reportAssignmentType=false