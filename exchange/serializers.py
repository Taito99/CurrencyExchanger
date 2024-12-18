from rest_framework import serializers
from .models import Exchange

class ExchangeRateSerializer(serializers.ModelSerializer):
    currency_pair = serializers.SerializerMethodField()
    exchange_rate = serializers.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        model = Exchange
        fields = ['currency_pair', 'exchange_rate']

    def get_currency_pair(self, obj):
        return f"{obj.base_currency.code}/{obj.target_currency.code}"
