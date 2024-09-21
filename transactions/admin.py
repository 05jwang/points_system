from django.contrib import admin
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    """
    Admin class for managing transactions.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        search_fields (tuple): Fields to search for in the admin search bar.
        list_filter (tuple): Fields to filter the admin list view by.
        ordering (tuple): Fields to order the admin list view by.
    """
    list_display = ('payer', 'points', 'timestamp')
    search_fields = ('payer', 'points')
    list_filter = ('payer', 'timestamp')
    ordering = ('-timestamp',)


admin.site.register(Transaction, TransactionAdmin)
