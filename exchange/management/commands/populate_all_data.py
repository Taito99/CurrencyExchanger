from django.core.management.base import BaseCommand
from exchange.utils import populate_exchange_rate

class Command(BaseCommand):
    def handle(self, *args, **options):
        populate_exchange_rate()
        self.stdout.write(self.style.SUCCESS('Successfully populated all data'))