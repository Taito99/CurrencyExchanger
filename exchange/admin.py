from openpyxl import Workbook
from django.http import HttpResponse
from django.contrib import admin
from .models import Exchange

def export_to_excel(modeladmin, request, queryset):
    """Export selected exchange rates to an XLSX file.

    Args:
        modeladmin: The current model admin instance.
        request: The HTTP request object.
        queryset: The queryset of selected Exchange objects.

    Returns:
        HttpResponse: A response containing the XLSX file.
    """
    # Create a new Excel workbook and active sheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Exchange Rates"

    # Write the header row
    sheet.append(['Base Currency', 'Target Currency', 'Exchange Rate', 'Date'])

    # Write data rows
    for exchange in queryset:
        sheet.append([
            exchange.base_currency.code,
            exchange.target_currency.code,
            float(exchange.exchange_rate),
            exchange.date.strftime('%Y-%m-%d')
        ])

    # Create an HTTP response with XLSX content
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="exchange_rates.xlsx"'

    # Save workbook to the response
    workbook.save(response)

    return response

export_to_excel.short_description = "Export selected exchange rates to XLSX"

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
