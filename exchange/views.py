#@Amadeusz Bujalski
from decimal import Decimal

from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.decorators import api_view
from django_filters import rest_framework as filters
from rest_framework.response import Response
from exchange.models import Exchange
from exchange.serializers import ExchangeRateSerializer
from exchange.utils import order_by_exchange_rate, get_5_exchange_rates
from rest_framework import generics


class ExchangeFilter(filters.FilterSet):
    base_currency = filters.CharFilter(field_name='base_currency__code', lookup_expr='iexact')
    target_currency = filters.CharFilter(field_name='target_currency__code', lookup_expr='iexact')

    class Meta:
        model = Exchange
        fields = ['base_currency', 'target_currency']

# Use the filter class in the ListAPIView
class ExchangeRateView(generics.ListAPIView):
    serializer_class = ExchangeRateSerializer
    queryset = Exchange.objects.all()
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ExchangeFilter



@api_view(['GET'])
def get_exchange_rate(request, base_currency, target_currency):
    """Retrieve the latest exchange rate for a specific currency pair.

    Args:
        request: The HTTP request object.
        base_currency (str): The base currency code (e.g., 'USD').
        target_currency (str): The target currency code (e.g., 'EUR').

    Returns:
        Response: JSON data containing the exchange rate or an error message.
    """
    exchange_rate = Exchange.objects.filter(
        base_currency__code=base_currency.upper(),
        target_currency__code=target_currency.upper()
    ).first()
    if not exchange_rate:
        return Response({'error': f'No exchange rate found for {base_currency}/{target_currency}'},
                        status=status.HTTP_404_NOT_FOUND)

    data = {
        "currency_pair": f"{base_currency}/{target_currency}",
        "exchange_rate": f"{exchange_rate.exchange_rate:.2f}",
    }
    return Response(data)


@extend_schema(
    parameters=[
        OpenApiParameter("amount", type=float, description="Amount of money to convert", required=True),
    ]
)
@api_view(['GET'])
def calculate_exchange(request, base_currency, target_currency):
        """Convert a specified amount of money from one currency to another.

        Args:
            request: The HTTP request object.
            base_currency (str): The base currency code (e.g., 'USD').
            target_currency (str): The target currency code (e.g., 'EUR').

        Returns:
            Response: JSON data containing the converted amount, exchange rate, and details.
        """
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
        ).first()

        if not exchange_rate:
            return Response(
                {'error': f'No exchange rate found for {base_currency}/{target_currency}'},
                status=status.HTTP_404_NOT_FOUND
            )

        converted_amount = amount * exchange_rate.exchange_rate

        return Response({
            "currency_pair": f"{base_currency}/{target_currency}",
            "amount": float(amount),
            "converted_amount": f"{float(converted_amount):.2f}",
            "exchange_rate": f"{float(exchange_rate.exchange_rate):.2f}"
        })

@api_view(['GET'])
def get_best_exchange_rate(request, base_currency):
    """Retrieve the best exchange rate for a given base currency.

    Args:
        request: The HTTP request object.
        base_currency (str): The base currency code (e.g., 'USD').

    Returns:
        Response: JSON data containing the target currency with the best rate or an error message.
    """
    exchanges = order_by_exchange_rate(base_currency).first()

    if not exchanges:
        return Response({'error': f'No exchange rate found for {base_currency}'}, status=status.HTTP_404_NOT_FOUND)

    return Response({
            "target_currency": exchanges.target_currency.code,
            "exchange_rate": f"{exchanges.exchange_rate:.2f}"
        })


@api_view(['GET'])
def get_worst_exchange_rate(request, base_currency):
    """Retrieve the worst exchange rate for a given base currency.

    Args:
        request: The HTTP request object.
        base_currency (str): The base currency code (e.g., 'USD').

    Returns:
        Response: JSON data containing the target currency with the worst rate or an error message.
    """
    exchanges = order_by_exchange_rate(base_currency).first()

    if not exchanges:
        return Response({'error': f'No exchange rate found for {base_currency}'}, status=status.HTTP_404_NOT_FOUND)

    return Response({
            "target_currency": exchanges.target_currency.code,
            "exchange_rate": f"{exchanges.exchange_rate:.2f}"
        })

@api_view(['GET'])
def get_top_5_best_exchange_rate(request, base_currency):
    """Retrieve the top 5 best exchange rates for a given base currency.

    Args:
        request: The HTTP request object.
        base_currency (str): The base currency code (e.g., 'USD').

    Returns:
        Response: JSON data containing the top 5 target currencies with the best rates or an error message.
    """
    exchanges = get_5_exchange_rates(base_currency, arg="best")

    if not exchanges:
        return Response({'error': f'No exchange rate found for {base_currency}'})

    results = [
        {
            "target_currency": exchange.target_currency.code,
            "exchange_rate": f"{exchanges.exchange_rate:.2f}"
        }
        for exchange in exchanges
    ]


    return Response({
        "currency": f"{base_currency}",
        "top 5 exchange rates": results
    })

@api_view(['GET'])
def get_top_5_worst_exchange_rate(request, base_currency):
    """Retrieve the top 5 worst exchange rates for a given base currency.

    Args:
        request: The HTTP request object.
        base_currency (str): The base currency code (e.g., 'USD').

    Returns:
        Response: JSON data containing the top 5 target currencies with the worst rates or an error message.
    """
    exchanges = get_5_exchange_rates(base_currency, arg="worst")

    if not exchanges:
        return Response({'error': f'No exchange rate found for {base_currency}'})

    results = [
        {
            "target_currency": exchange.target_currency.code,
            "exchange_rate": f"{exchanges.exchange_rate:.2f}"
        }
        for exchange in exchanges
    ]


    return Response({
        "currency": f"{base_currency}",
        "top 5 exchange rates": results
    })
