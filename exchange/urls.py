#@Amadeusz Bujalski
from django.urls import path
from django_filters.views import FilterView

from .models import Exchange
from .views import ExchangeFilter, ExchangeRateView, get_exchange_rate, calculate_exchange, get_worst_exchange_rate, \
    get_top_5_worst_exchange_rate, get_top_5_best_exchange_rate, get_best_exchange_rate

urlpatterns = [
    path('currency/usd-to-eur/', get_exchange_rate, {'base_currency': 'USD', 'target_currency': 'EUR'}, name='currency_usd_to_eur'),
    path('currency/eur-to-usd/', get_exchange_rate, {'base_currency': 'EUR', 'target_currency': 'USD'}, name='currency_eur_to_usd'),
    path('currency/usd-to-pln/', get_exchange_rate, {'base_currency': 'USD', 'target_currency': 'PLN'}, name='currency_usd_to_pln'),
    path('currency/eur-to-pln/', get_exchange_rate, {'base_currency': 'EUR', 'target_currency': 'PLN'}, name='currency_eur_to_pln'),

    path('currency/best/<str:base_currency>/', get_best_exchange_rate, name='currency_best_exchange'),
    path('currency/top5-best/<str:base_currency>/', get_top_5_best_exchange_rate, name='currency_top5_best_exchange'),
    path('currency/top5-worst/<str:base_currency>/', get_top_5_worst_exchange_rate, name='currency_top5_worst_exchange'),
    path('currency/worst/<str:base_currency>/', get_worst_exchange_rate, name='currency_worst_exchange'),

    path('currency/<str:base_currency>/<str:target_currency>/', get_exchange_rate, name='currency_exchange_rate'),

    path('currency/calculate-exchange/<str:base_currency>/<str:target_currency>/', calculate_exchange, name='currency_convert_rate'),

    path('currency/filter/', ExchangeRateView.as_view(), name='currency_filter_by_base_target'),
]
