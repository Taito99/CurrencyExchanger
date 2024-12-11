from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from exchange.models import Exchange
from exchange.serializers import ExchangeRateSerializer
from decimal import Decimal


@api_view(['GET'])
def get_exchange_rate(request, base_currency, target_currency):
    exchange_rate = Exchange.objects.filter(
        base_currency__code=base_currency.upper(),
        target_currency__code=target_currency.upper()
    ).last()
    if not exchange_rate:
        return Response({'error': f'No exchange rate found for {base_currency}/{target_currency}'},
                        status=status.HTTP_404_NOT_FOUND)

    data = {
        "currency_pair": f"{base_currency}/{target_currency}",
        "exchange_rate": exchange_rate.exchange_rate,
    }
    serializer = ExchangeRateSerializer(data)
    return Response(serializer.data)


@extend_schema(
    parameters=[
        OpenApiParameter("amount", type=float, description="Amount of money to convert", required=True),
    ]
)
@api_view(['GET'])
def convert_currency(request, base_currency, target_currency):
    amount = request.query_params.get('amount')
    if not amount:
        return Response(
            {'error': "Amount is required as a query parameter, e.g., ?amount=100"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        amount = Decimal(amount)
    except (ValueError, TypeError):
        return Response(
            {'error': "Amount must be a valid number"},
            status=status.HTTP_400_BAD_REQUEST
        )

    exchange_rate = Exchange.objects.filter(
        base_currency__code=base_currency.upper(),
        target_currency__code=target_currency.upper()
    ).last()

    if not exchange_rate:
        return Response(
            {'error': f'No exchange rate found for {base_currency}/{target_currency}'},
            status=status.HTTP_404_NOT_FOUND
        )

    converted_amount = amount * exchange_rate.exchange_rate

    return Response({
        "currency_pair": f"{base_currency}/{target_currency}",
        "amount": float(amount),
        "converted_amount": float(converted_amount),  # Konwersja Decimal na float w odpowiedzi
        "exchange_rate": float(exchange_rate.exchange_rate)
    })
