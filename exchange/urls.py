from django.urls import path

from .views import get_exchange_rate, convert_currency, get_best_exchange_rate, get_worst_exchange_rate, \
    get_top_5_best_exchange_rate, get_top_5_worst_exchange_rate

urlpatterns = [
    path('currency/USD/EUR/', get_exchange_rate, {'base_currency': 'USD', 'target_currency': 'EUR'}, name='get_usd_to_eur'),
    path('currency/EUR/USD/', get_exchange_rate, {'base_currency': 'EUR', 'target_currency': 'USD'}, name='get_eur_to_usd'),
    path('currency/USD/PLN/', get_exchange_rate, {'base_currency': 'USD', 'target_currency': 'PLN'}, name='get_usd_to_pln'),
    path('currency/EUR/PLN/', get_exchange_rate, {'base_currency': 'EUR', 'target_currency': 'PLN'}, name='get_eur_to_pln'),

    path('currency/best-exchange/<str:base_currency>/', get_best_exchange_rate, name='best_exchange_rate'),
    path('currency/top5-best-exchange/<str:base_currency>/', get_top_5_best_exchange_rate, name='top5_best_exchange_rate'),
    path('currency/top5-worst-exchange/<str:base_currency>/', get_top_5_worst_exchange_rate, name='top5_worst_exchange_rate'),
    path('currency/worst-exchange/<str:base_currency>/', get_worst_exchange_rate, name='worst_exchange_rate'),

    path('currency/<str:base_currency>/<str:target_currency>/', get_exchange_rate, name='get_exchange_rate'),

    path('currency/convert/<str:base_currency>/<str:target_currency>/', convert_currency, name='convert_currency'),

]
