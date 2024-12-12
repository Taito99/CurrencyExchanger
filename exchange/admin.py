#@Amadeusz Bujalski
import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Exchange

def export_to_excel(modeladmin, request, queryset):
    """Export selected exchange rates to a CSV file.

    Args:
        modeladmin: The current model admin instance.
        request: The HTTP request object.
        queryset: The queryset of selected Exchange objects.

    Returns:
        HttpResponse: A response containing the CSV file.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exchange_rates.csv"'
    writer = csv.writer(response, delimiter=';')

    # Write the header row
    writer.writerow(['Base Currency', 'Target Currency', 'Exchange Rate', 'Date'])

    # Write data rows
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
    """Admin interface for managing Exchange objects.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        list_filter (tuple): Fields to filter the list view.
        search_fields (tuple): Fields to enable search functionality.
        actions (list): Custom actions for the admin interface.
    """
    list_display = ('id', 'base_currency', 'target_currency', 'exchange_rate', 'date')
    list_filter = ('base_currency', 'target_currency', 'date')
    search_fields = ('base_currency__code', 'target_currency__code')
    actions = [export_to_excel]
