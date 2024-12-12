#@Amadeusz Bujalski
from unittest.mock import patch
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from currency.models import Currency
from exchange.models import Exchange


class CommandsTestCase(TestCase):
    """Test custom Django management commands"""

    @patch('exchange.management.commands.populate_currencies.Command.handle')
    def test_populate_currencies_command(self, mock_handle):
        """Test the populate_currencies command"""
        mock_handle.return_value = None

        call_command('populate_currencies')

        mock_handle.assert_called_once()

    @patch('exchange.management.commands.populate_all_data.Command.handle')
    def test_populate_all_data_command(self, mock_handle):
        """Test the populate_all_data command"""
        mock_handle.return_value = None

        call_command('populate_all_data')

        mock_handle.assert_called_once()

    @patch('exchange.management.commands.populate_all_data.populate_exchange_rate')
    def test_populate_exchange_rate_function_called(self, mock_populate_exchange_rate):
        """Test that populate_exchange_rate function is called in the command"""
        mock_populate_exchange_rate.return_value = None

        call_command('populate_all_data')

        mock_populate_exchange_rate.assert_called_once()

class ExchangeModelTests(TestCase):
    """Test the Exchange model"""

    @classmethod
    def setUpTestData(cls):
        """Set up test data once for all tests"""
        cls.currency_usd = Currency.objects.create(code="USD", name="US Dollar")
        cls.currency_eur = Currency.objects.create(code="EUR", name="Euro")

    def test_create_exchange_successful(self):
        """Test creating an exchange rate is successful"""
        exchange = Exchange.objects.create(
            base_currency=self.currency_usd,
            target_currency=self.currency_eur,
            exchange_rate=1.1234
        )

        self.assertEqual(exchange.base_currency, self.currency_usd)
        self.assertEqual(exchange.target_currency, self.currency_eur)
        self.assertEqual(exchange.exchange_rate, 1.1234)
        self.assertEqual(str(exchange), "USD/EUR - 1.1234")

    def test_exchange_string_representation(self):
        """Test the string representation of an exchange"""
        exchange = Exchange.objects.create(
            base_currency=self.currency_usd,
            target_currency=self.currency_eur,
            exchange_rate=0.9876
        )

        self.assertEqual(str(exchange), "USD/EUR - 0.9876")

    def test_exchange_base_and_target_currencies(self):
        """Test that base and target currencies are correctly assigned"""
        exchange = Exchange.objects.create(
            base_currency=self.currency_usd,
            target_currency=self.currency_eur,
            exchange_rate=1.0000
        )

        self.assertEqual(exchange.base_currency.code, "USD")
        self.assertEqual(exchange.target_currency.code, "EUR")

class URLTests(TestCase):
    """Tests for the exchange-related URLs"""

    @classmethod
    def setUpTestData(cls):
        """Set up test data once for all tests"""
        cls.client = APIClient()
        cls.currency_usd = Currency.objects.create(code="USD", name="US Dollar")
        cls.currency_eur = Currency.objects.create(code="EUR", name="Euro")
        cls.currency_pln = Currency.objects.create(code="PLN", name="Polish Zloty")

        cls.exchange = Exchange.objects.create(
            base_currency=cls.currency_usd,
            target_currency=cls.currency_eur,
            exchange_rate=1.1234
        )

    def test_get_exchange_rate(self):
        """Test retrieving a specific exchange rate"""
        url = reverse('get_exchange_rate', args=["USD", "EUR"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("exchange_rate", response.data)

    def test_convert_currency(self):
        """Test converting currency with a specific amount"""
        url = reverse('convert_currency', args=["USD", "EUR"])
        response = self.client.get(url, {"amount": 100})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("converted_amount", response.data)

    def test_convert_currency_negative_amount(self):
        """Test converting currency with a negative amount"""
        url = reverse('convert_currency', args=["USD", "EUR"])
        response = self.client.get(url, {"amount": -100})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_convert_currency_zero_amount(self):
        """Test converting currency with an amount of zero"""
        url = reverse('convert_currency', args=["USD", "EUR"])
        response = self.client.get(url, {"amount": 0})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_get_best_exchange_rate(self):
        """Test retrieving the best exchange rate for a base currency"""
        url = reverse('best_exchange_rate', args=["USD"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("exchange_rate", response.data)

    def test_get_worst_exchange_rate(self):
        """Test retrieving the worst exchange rate for a base currency"""
        url = reverse('worst_exchange_rate', args=["USD"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("exchange_rate", response.data)

    def test_get_top_5_best_exchange_rate(self):
        """Test retrieving the top 5 best exchange rates for a base currency"""
        url = reverse('top5_best_exchange_rate', args=["USD"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("top 5 exchange rates", response.data)

    def test_get_top_5_worst_exchange_rate(self):
        """Test retrieving the top 5 worst exchange rates for a base currency"""
        url = reverse('top5_worst_exchange_rate', args=["USD"])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("top 5 exchange rates", response.data)


