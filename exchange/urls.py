from django.urls import path
from .views import get_exchange_rate, convert_currency

urlpatterns = [
    path('currency/USD/EUR/', get_exchange_rate, {'base_currency': 'USD', 'target_currency': 'EUR'}, name='get_usd_to_eur'),
    path('currency/EUR/USD/', get_exchange_rate, {'base_currency': 'EUR', 'target_currency': 'USD'}, name='get_eur_to_usd'),
    path('currency/USD/PLN/', get_exchange_rate, {'base_currency': 'USD', 'target_currency': 'PLN'}, name='get_usd_to_pln'),
    path('currency/EUR/PLN/', get_exchange_rate, {'base_currency': 'EUR', 'target_currency': 'PLN'}, name='get_eur_to_pln'),

    path('currency/<str:base_currency>/<str:target_currency>/', get_exchange_rate, name='get_exchange_rate'),

    path('currency/convert/<str:base_currency>/<str:target_currency>/', convert_currency, name='convert_currency'),
]
