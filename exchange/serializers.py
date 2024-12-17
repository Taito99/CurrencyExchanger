#@Amadeusz Bujalski
from rest_framework import serializers
from exchange.models import Exchange

class ExchangeRateSerializer(serializers.Serializer):
    """Serializer for a single exchange rate.

    Fields:
        currency_pair (str): The currency pair (e.g., "USD/EUR").
        exchange_rate (Decimal): The exchange rate between the base and target currencies.
    """
    currency_pair = serializers.CharField()
    exchange_rate = serializers.DecimalField(max_digits=10, decimal_places=4)

