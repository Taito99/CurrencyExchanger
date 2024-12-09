from django.db import models

from currency.models import Currency


# Create your models here.

class Exchange(models.Model):
    base_currency = models.ForeignKey(Currency, related_name='base_exchange_rate', on_delete=models.CASCADE)
    target_currency = models.ForeignKey(Currency, related_name='target_exchange_rate', on_delete=models.CASCADE)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateField(auto_now_add=True)
    currency_pair = models.CharField(max_length=7, blank=True, null=True)

    def save(self, *args, **kwargs):
        #Automaticly generating currency_pair in format Base/Target
        if not self.currency_pair:
            self.currency_pair = f"{self.base_currency.code}/{self.target_currency.code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.currency_pair} - {self.exchange_rate}"


