from logging import raiseExceptions

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

def clean_old_exchange_rates():
    deleted_count, _ = Exchange.objects.exclude(date=now().date()).delete()
    print(f"Deleted {deleted_count} outdated exchange rate records.")



def populate_exchange_rate():
    clean_old_exchange_rates()
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

def order_by_exchange_rate(base_currency):
    return Exchange.objects.filter(
        base_currency__code=base_currency.upper()
    ).order_by('-exchange_rate')

def get_5_exchange_rates(base_currency, arg="best"):
    if arg.lower() == "best":
        return order_by_exchange_rate(base_currency)[:5]
    elif arg.lower() == "worst":
        return order_by_exchange_rate(base_currency).reverse()[:5]
    else:
        raise ValueError("Invalid argument. You must use 'best' or 'worst'.")

