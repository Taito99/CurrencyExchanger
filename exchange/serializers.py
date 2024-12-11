from rest_framework import serializers
from exchange.models import Exchange


class ExchangeSerializer(serializers.ModelSerializer):
    base_currency = serializers.CharField(source='base_currency.code', read_only=True)
    target_currency = serializers.CharField(source='target_currency.code', read_only=True)

    class Meta:
        model = Exchange
        fields = ['id', 'base_currency', 'target_currency', 'exchange_rate', 'date']
        read_only_fields = ['id', 'base_currency', 'target_currency', 'exchange_rate', 'date']

class ExchangeRateSerializer(serializers.Serializer):
    currency_pair = serializers.CharField()
    exchange_rate = serializers.DecimalField(max_digits=10, decimal_places=4)

class ConvertedCurrencySerializer(serializers.Serializer):
    currency_pair = serializers.CharField()
    amount = serializers.FloatField()
    converted_amount = serializers.FloatField()
    exchange_rate = serializers.DecimalField(max_digits=10, decimal_places=4)
