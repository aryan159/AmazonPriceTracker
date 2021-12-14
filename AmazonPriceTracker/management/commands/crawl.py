from django.core.management.base import BaseCommand, CommandError
from AmazonPriceTracker.once_per_day_scraper import OncePerDayScraper

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    """ def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int) """

    def handle(self, *args, **options):
        OncePerDayScraper()
        self.stdout.write(self.style.SUCCESS('OncePerDayScraper() Ended'))