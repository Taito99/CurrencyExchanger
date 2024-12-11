import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Exchange


def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exchange_rates.csv"'
    writer = csv.writer(response , delimiter=';')

    writer.writerow(['Base Currency', 'Target Currency', 'Exchange Rate', 'Date'])

    for exchange in queryset:
        writer.writerow([
            exchange.base_currency.code,
            exchange.target_currency.code,
            float(exchange.exchange_rate),
            exchange.date.strftime('%Y-%m-%d')
        ])

    return response


export_to_excel.short_description = "Export selected exchange rates to CSV"


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'base_currency', 'target_currency', 'exchange_rate', 'date')
    list_filter = ('base_currency', 'target_currency', 'date')
    search_fields = ('base_currency__code', 'target_currency__code')

    actions = [export_to_excel]
