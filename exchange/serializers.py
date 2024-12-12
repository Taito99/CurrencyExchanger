from rest_framework import serializers
from exchange.models import Exchange

class ExchangeSerializer(serializers.ModelSerializer):
    """Serializer for the Exchange model.

    Fields:
        base_currency (str): Code of the base currency (e.g., "USD").
        target_currency (str): Code of the target currency (e.g., "EUR").
        exchange_rate (Decimal): The exchange rate between base and target currencies.
        date (date): The date when the exchange rate was recorded.
    """
    base_currency = serializers.CharField(source='base_currency.code', read_only=True)
    target_currency = serializers.CharField(source='target_currency.code', read_only=True)

    class Meta:
        model = Exchange
        fields = ['id', 'base_currency', 'target_currency', 'exchange_rate', 'date']
        read_only_fields = ['id', 'base_currency', 'target_currency', 'exchange_rate', 'date']

class ExchangeRateSerializer(serializers.Serializer):
    """Serializer for a single exchange rate.

    Fields:
        currency_pair (str): The currency pair (e.g., "USD/EUR").
        exchange_rate (Decimal): The exchange rate between the base and target currencies.
    """
    currency_pair = serializers.CharField()
    exchange_rate = serializers.DecimalField(max_digits=10, decimal_places=4)

class ConvertedCurrencySerializer(serializers.Serializer):
    """Serializer for converting currency amounts.

    Fields:
        currency_pair (str): The currency pair (e.g., "USD/EUR").
        amount (float): The amount of money to convert.
        converted_amount (float): The converted amount in the target currency.
        exchange_rate (Decimal): The exchange rate used for the conversion.
    """
    currency_pair = serializers.CharField()
    amount = serializers.FloatField()
    converted_amount = serializers.FloatField()
    exchange_rate = serializers.DecimalField(max_digits=10, decimal_places=4)

class BaseCurrencySerializer(serializers.ModelSerializer):
    """Serializer for the base currency field of an Exchange.

    Fields:
        base_currency (str): Code of the base currency (e.g., "USD").
    """
    base_currency = serializers.CharField(source='base_currency.code', read_only=True)

    class Meta:
        model = Exchange
        fields = ['base_currency']
        read_only_fields = ['base_currency']
