from django.core.management.base import BaseCommand

class Command(BaseCommand):
    message = 'Hello'

    def handle(self, *args, **options):
        self.stdout.write(self.message + ' from custom command')