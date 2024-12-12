from django.db import models
from currency.models import Currency

class Exchange(models.Model):
    """Model representing an exchange rate between two currencies.

    Attributes:
        base_currency (ForeignKey): The currency being converted from.
        target_currency (ForeignKey): The currency being converted to.
        exchange_rate (DecimalField): The rate of exchange between the two currencies.
        date (DateField): The date when the exchange rate was recorded.
    """
    base_currency = models.ForeignKey(
        Currency,
        related_name='base_exchange_rate',
        on_delete=models.CASCADE
    )
    target_currency = models.ForeignKey(
        Currency,
        related_name='target_exchange_rate',
        on_delete=models.CASCADE
    )
    exchange_rate = models.DecimalField(
        max_digits=10,
        decimal_places=4
    )
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        """String representation of the exchange rate."""
        return f"{self.base_currency.code}/{self.target_currency.code} - {self.exchange_rate}"
