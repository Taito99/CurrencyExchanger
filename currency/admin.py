#@Amadeusz Bujalski
from django.contrib import admin
from currency.models import Currency

# Register your models here.

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')
    search_fields = ('code', 'name')
