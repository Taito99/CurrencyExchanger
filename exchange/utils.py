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
        print("No currencies found in the database.")
        return

    pairs = permutations(currencies, 2)
    updated_count = 0
    failed_pairs = []

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
                updated_count += 1
            except Exception as e:
                print(f"Error updating exchange rate for {base_currency.code}/{target_currency.code}: {e}")
        else:
            failed_pairs.append(f"{base_currency.code}/{target_currency.code}")

    print(f"Successfully updated {updated_count} exchange rates.")
    if failed_pairs:
        print(f"Failed to fetch rates for the following pairs: {', '.join(failed_pairs)}, no exchange rates found in yahoo finance api")
