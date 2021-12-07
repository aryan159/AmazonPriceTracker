from django.core.management.base import BaseCommand, CommandError
from AmazonPriceTracker.daily_web_scraper import DailyWebScraper

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    """ def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int) """

    def handle(self, *args, **options):
        DailyWebScraper()
        self.stdout.write(self.style.SUCCESS('DailyWebScraper() Ended'))