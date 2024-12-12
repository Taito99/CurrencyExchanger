from django.test import TestCase
from currency.models import Currency

class CurrencyModelTests(TestCase):
    """
    Test cases for the Currency model.

    This test suite verifies the functionality and constraints of the `Currency` model,
    including successful creation, uniqueness of currency codes, and the string representation
    of the model.

    Methods:
        test_create_currency_successful: Verifies that a new currency can be created successfully.
        test_create_currency_without_name: Ensures that a currency can be created without a name.
        test_currency_code_unique: Validates that currency codes must be unique.
        test_currency_string_representation: Confirms that the string representation of the
                                             model is correct, defaulting to the name or code.
    """

    def test_create_currency_successful(self):
        """
        Test creating a new currency is successful.

        This test ensures that a new `Currency` instance with a valid `code` and `name`
        is created successfully.
        """
        code = "USD"
        name = "United States Dollar"
        currency = Currency.objects.create(code=code, name=name)

        self.assertEqual(currency.code, code)
        self.assertEqual(currency.name, name)
        self.assertEqual(str(currency), name)

    def test_create_currency_without_name(self):
        """
        Test creating a currency without a name is successful.

        This test checks that a `Currency` instance can be created with a `code` only,
        and the `name` is set to `None`. The string representation defaults to the `code`.
        """
        code = "EUR"
        currency = Currency.objects.create(code=code, name=None)

        self.assertEqual(currency.code, code)
        self.assertIsNone(currency.name)
        self.assertEqual(str(currency), code)

    def test_currency_code_unique(self):
        """
        Test that currency codes are unique.

        This test ensures that creating a second `Currency` instance with the same `code`
        raises an exception.
        """
        code = "USD"
        name1 = "United States Dollar"
        name2 = "Duplicate Dollar"

        Currency.objects.create(code=code, name=name1)
        with self.assertRaises(Exception):
            Currency.objects.create(code=code, name=name2)

    def test_currency_string_representation(self):
        """
        Test the string representation of a currency.

        This test ensures that the string representation of a `Currency` instance is the
        `name` when available, otherwise it defaults to the `code`.
        """
        currency = Currency.objects.create(code="GBP", name="British Pound")

        self.assertEqual(str(currency), "British Pound")
