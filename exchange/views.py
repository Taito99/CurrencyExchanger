from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from exchange.models import Exchange
from exchange.serializers import ExchangeRateSerializer, BaseCurrencySerializer
from decimal import Decimal

from exchange.utils import order_by_exchange_rate, get_5_exchange_rates


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
        "exchange_rate": round(exchange_rate.exchange_rate, 2),
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
        if amount <= 0:
            return Response(
                {'error': "Amount must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST
            )
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
        "converted_amount": round(float(converted_amount), 2),
        "exchange_rate": round(float(exchange_rate.exchange_rate), 2)
    })


@api_view(['GET'])
def get_best_exchange_rate(request, base_currency):
    exchanges = order_by_exchange_rate(base_currency).first()

    if not exchanges:
        return Response({'error': f'No exchange rate found for {base_currency}'}, status=status.HTTP_404_NOT_FOUND)

    return Response({
            "target_currency": exchanges.target_currency.code,
            "exchange_rate": round(float(exchanges.exchange_rate), 2)
        })



@api_view(['GET'])
def get_worst_exchange_rate(request, base_currency):
    exchanges = order_by_exchange_rate(base_currency).last()

    if not exchanges:
        return Response({'error': f'No exchange rate found for {base_currency}'}, status=status.HTTP_404_NOT_FOUND)

    return Response({
            "target_currency": exchanges.target_currency.code,
            "exchange_rate": round(float(exchanges.exchange_rate), 2)
        })

@api_view(['GET'])
def get_top_5_best_exchange_rate(request, base_currency):
    exchanges = get_5_exchange_rates(base_currency, arg="best")

    if not exchanges:
        return Response({'error': f'No exchange rate found for {base_currency}'})

    results = [
        {
            "target_currency": exchange.target_currency.code,
            "exchange_rate": round(float(exchange.exchange_rate), 2)
        }
        for exchange in exchanges
    ]


    return Response({
        "currency": f"{base_currency}",
        "top 5 exchange rates": results
    })

@api_view(['GET'])
def get_top_5_worst_exchange_rate(request, base_currency):
    exchanges = get_5_exchange_rates(base_currency, arg="worst")

    if not exchanges:
        return Response({'error': f'No exchange rate found for {base_currency}'})

    results = [
        {
            "target_currency": exchange.target_currency.code,
            "exchange_rate": round(float(exchange.exchange_rate), 2)
        }
        for exchange in exchanges
    ]


    return Response({
        "currency": f"{base_currency}",
        "top 5 exchange rates": results
    })




