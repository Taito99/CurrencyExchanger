from rest_framework import serializers
from exchange.models import Exchange


class ExchangeSerializer(serializers.ModelSerializer):
    base_currency = serializers.CharField(source='base_currency.code', read_only=True)
    target_currency = serializers.CharField(source='target_currency.code', read_only=True)

    class Meta:
        model = Exchange
        fields = ['id', 'base_currency', 'target_currency', 'exchange_rate', 'date']
        read_only_fields = ['id', 'base_currency', 'target_currency', 'exchange_rate', 'date']
