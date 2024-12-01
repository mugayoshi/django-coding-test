import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings

from myapp.services.channel_rating_service import calculate_channel_ratings

class Command(BaseCommand):
    help = 'Export channel ratings to a CSV file, sorted from highest to lowest'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output', 
            type=str, 
            help='Custom output file path', 
            default=os.path.join(settings.BASE_DIR, 'channel_ratings.csv')
        )

    def handle(self, *args, **options):
        output_path = options['output']
        channels = calculate_channel_ratings()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Channel Title', 'Average Rating'])

            for channel in channels:
                csv_writer.writerow([
                    channel.title, 
                    f"{channel.avg_rating:.2f}"
                ])

        self.stdout.write(self.style.SUCCESS(
            f'Successfully exported channel ratings to {output_path}'
        ))
