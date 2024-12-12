#@Amadeusz Bujalski
from rest_framework import serializers
from currency.models import Currency

class CurrencySerializer(serializers.ModelSerializer):
    """
    Serializer for the Currency model.

    This serializer is used to convert `Currency` model instances into JSON format
    and vice versa. It defines the fields to be serialized and deserialized and
    marks them as read-only since the `Currency` model data is immutable.

    Fields:
        id (int): The unique identifier of the currency.
        code (str): The currency code (e.g., "USD").
        name (str): The full name of the currency (e.g., "United States Dollar").

    Meta:
        model (Currency): The `Currency` model that this serializer works with.
        fields (list): Specifies the fields to include in the serialized data.
        read_only_fields (list): Marks all fields as read-only to prevent updates or creation
                                 through this serializer.
    """
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name']
        read_only_fields = ['id', 'code', 'name']
