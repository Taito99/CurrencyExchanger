#@Amadeusz Bujalski
from itertools import permutations
import yfinance as yf
from django.utils.timezone import now
from currency.models import Currency
from exchange.models import Exchange


def fetch_exchange_rate(base_currency, target_currency):
    """Fetch the latest exchange rate for a given currency pair from Yahoo Finance.

    Args:
        base_currency (Currency): The base currency object.
        target_currency (Currency): The target currency object.

    Returns:
        float: The exchange rate if found, otherwise None.
    """
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
    """Delete outdated exchange rate records from the database.

    Deletes all exchange rate records that are not for the current date.
    """
    deleted_count, _ = Exchange.objects.exclude(date=now().date()).delete()
    print(f"Deleted {deleted_count} outdated exchange rate records.")

def populate_exchange_rate():
    """Fetch and populate exchange rates for all currency pairs in the database.

    Retrieves exchange rates for all permutations of currencies stored in the database,
    updates the database with the latest rates, and cleans old data.
    """
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
        print(f"Failed to fetch rates for the following pairs: {', '.join(failed_pairs)}, no exchange rates found in Yahoo Finance API")

def order_by_exchange_rate(base_currency):
    """Order exchange rates for a given base currency in descending order.

    Args:
        base_currency (str): The base currency code.

    Returns:
        QuerySet: A QuerySet of Exchange objects ordered by exchange rate.
    """
    return Exchange.objects.filter(
        base_currency__code=base_currency.upper()
    ).order_by('-exchange_rate')

def get_5_exchange_rates(base_currency, arg="best"):
    """Retrieve the top 5 best or worst exchange rates for a given base currency.

    Args:
        base_currency (str): The base currency code.
        arg (str, optional): Determines whether to fetch the "best" or "worst" rates. Defaults to "best".

    Returns:
        QuerySet: A QuerySet of up to 5 Exchange objects matching the criteria.
    """
    if arg.lower() == "best":
        return order_by_exchange_rate(base_currency)[:5]
    elif arg.lower() == "worst":
        return order_by_exchange_rate(base_currency).reverse()[:5]
    else:
        raise ValueError("Invalid argument. You must use 'best' or 'worst'.")
