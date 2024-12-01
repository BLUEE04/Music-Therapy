from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

try:
    with transaction.atomic():
        # Check if a superuser already exists
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='stuffmayhappen',
                email='walter.santos.quinta5466@gmail.com',
                password='Walter.0507.Sara!'
            )
            print("Superuser created successfully!")
        else:
            print("Superuser already exists.")
except Exception as e:
    print(f"An error occurred: {e}")
