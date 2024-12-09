import yfinance as yf
from itertools import permutations

from django.utils.timezone import now

from currency.models import Currency
from exchange.models import Exchange


def fetch_exchange_rate(base_currency, target_currency):
    pair = f"{base_currency.code}{target_currency.code}=X"
    ticker = yf.Ticker(pair)

    try:
        data = ticker.history(period="1d")
        if not data.empty:
            rate = data['Close'].iloc[-1]
            return rate
        else:
            print(f"No data found for pair: {pair}")
    except Exception as e:
        print(f"Error fetching data for pair {pair}: {e}")
    return None


def populate_exchange_rate():
    currencies = Currency.objects.all()

    if not currencies.exists():
        return

    pairs = permutations(currencies, 2)

    for base_currency, target_currency in pairs:
        rate = fetch_exchange_rate(base_currency, target_currency)

        if rate:
            try:
                Exchange.objects.update_or_create(
                    base_currency=base_currency,
                    target_currency=target_currency,
                    date=now().date(),
                    defaults={'exchange_rate': rate}
                )
            except Exception as e:
                print(f"Error updating exchange rate: {e}")
        else:
            print(f"Failed to fetch rate for {base_currency.code}/{target_currency.code}")

