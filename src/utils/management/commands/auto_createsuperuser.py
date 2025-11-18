from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from decouple import config

class Command(BaseCommand):
    help = 'Automatically creates a superuser if one does not exist.'

    def handle(self, *args, **options):
        USERNAME : str = config("DJANGO_SUPERUSER_USERNAME",cast=str ,default= "admin")
        EMAIL : str = config("DJANGO_SUPERUSER_EMAIL",cast=str ,default= "admin@example.com")
        PASSWORD : str = config("DJANGO_SUPERUSER_PASSWORD",cast=str ,default= "admin")
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser name : {USERNAME}'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
            

# pyright: reportAssignmentType=false