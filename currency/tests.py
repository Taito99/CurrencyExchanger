from django.test import TestCase
from currency.models import Currency

#Test model
class CurrencyModelTests(TestCase):
    """Tests for the Currency model"""

    def test_create_currency_successful(self):
        """Test creating a new currency is successful"""
        code = "USD"
        name = "United States Dollar"
        currency = Currency.objects.create(
            code=code,
            name=name
        )

        self.assertEqual(currency.code, code)
        self.assertEqual(currency.name, name)
        self.assertEqual(str(currency), name)

    def test_create_currency_without_name(self):
        """Test creating a currency without a name is successful"""
        code = "EUR"
        currency = Currency.objects.create(
            code=code,
            name=None
        )

        self.assertEqual(currency.code, code)
        self.assertIsNone(currency.name)
        self.assertEqual(str(currency), code)

    def test_currency_code_unique(self):
        """Test that currency codes are unique"""
        code = "USD"
        name1 = "United States Dollar"
        name2 = "Duplicate Dollar"

        Currency.objects.create(code=code, name=name1)
        with self.assertRaises(Exception):
            Currency.objects.create(code=code, name=name2)

    def test_currency_string_representation(self):
        """Test the string representation of a currency"""
        currency = Currency.objects.create(
            code="GBP",
            name="British Pound"
        )

        self.assertEqual(str(currency), "British Pound")