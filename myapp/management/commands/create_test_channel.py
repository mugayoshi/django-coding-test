import random
from django.core.management.base import BaseCommand
from myapp.models import Channel
from .utils import create_test_content_with_files

class Command(BaseCommand):
    help = "Creates a test channel with its contents and files for testing purposes."
    def add_arguments(self, parser):
        parser.add_argument('--title', type=str, help='Channel title', default='Test Channel')
        parser.add_argument('--language', type=str, help='Channel language', default='English')
        parser.add_argument('--content-count', type=int, help='Number of contents to create', default=3)

    def handle(self, *args, **kwargs):
        channel_title = kwargs['title']
        channel_language = kwargs['language']
        content_count = kwargs['content_count']

        channel = Channel.objects.create(
            title=channel_title,
            language=channel_language
        )
        for i in range(content_count):
            content = create_test_content_with_files(
                title=f'{channel_title} Content {i+1}',
                metadata={
                    'description': f'Test description for content {i+1}',
                    'source': 'Management Command'
                },
                files_count=2,
                rating=round(random.uniform(0, 10), 2)
            )
            channel.contents.add(content)
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created channel "{channel_title}" '
            f'with {content_count} contents'
        ))

