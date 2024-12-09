from rest_framework import serializers
from currency.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name']
        read_only_fields = ['id', 'code', 'name']
