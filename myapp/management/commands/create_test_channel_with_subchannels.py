import random
from django.core.management.base import BaseCommand
from myapp.models import Channel, Content, ContentFile
from .utils import create_test_content_with_files

class Command(BaseCommand):
    help = "Creates a test channel with multiple subchannels for testing purposes."

    def add_arguments(self, parser):
        parser.add_argument(
            '--main-channel-title', 
            type=str, 
            help='Title of the main channel', 
            default='Sports Network'
        )
        parser.add_argument(
            '--subchannel-count', 
            type=int, 
            help='Number of subchannels to create', 
            default=3
        )

    def handle(self, *args, **kwargs):
        main_channel = Channel.objects.create(
            title=kwargs['main_channel_title'],
            language='English'
        )

        subchannels = []
        for i in range(kwargs['subchannel_count']):
            subchannel_title = f"{main_channel.title} - Subchannel {i+1}"
            subchannel = Channel.objects.create(
                title=subchannel_title,
                language='English',
                parent_channel=main_channel
            )
            for i in range(random.randrange(1,4)):
                content = create_test_content_with_files(
                    title=f"{subchannel_title}_content {i+1}",
                    metadata={
                        'description': f'Test description for content {i+1}',
                        'source': 'Management Command'
                    },
                    files_count=2,
                    rating=round(random.uniform(0, 10), 2)
                )
                subchannel.contents.add(content)

            subchannels.append(subchannel)
        
        self.stdout.write(self.style.SUCCESS(
            f"Created main channel '{main_channel.title}' with {len(subchannels)} subchannels:"
        ))

        for subchannel in subchannels:
            self.stdout.write(f" - {subchannel.title}")