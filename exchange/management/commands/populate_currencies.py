from django.core.management.base import BaseCommand
from currency.models import Currency

class Command(BaseCommand):
    def handle(self, *args, **options):
        currencies = [
            {'code': 'USD', 'name': 'US Dollar'},
            {'code': 'EUR', 'name': 'Euro'},
            {'code': 'PLN', 'name': 'Polish Zloty'},
            {'code': 'GBP', 'name': 'British Pound'},
            {'code': 'JPY', 'name': 'Japanese Yen'},
            {'code': 'AUD', 'name': 'Australian Dollar'},
            {'code': 'CAD', 'name': 'Canadian Dollar'},
            {'code': 'CHF', 'name': 'Swiss Franc'},
            {'code': 'CNY', 'name': 'Chinese Yuan'},
            {'code': 'SEK', 'name': 'Swedish Krona'},
        ]
        for currency in currencies:
            obj, created = Currency.objects.get_or_create(
                code=currency['code'],
                defaults={'name': currency['name']}
            )
            if not created:
                self.stdout.write(f"The currency '{currency['name']}' already exists.")
            else:
                self.stdout.write(self.style.SUCCESS(f"The currency '{currency['code']}' has been created."))