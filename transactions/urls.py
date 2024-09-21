from django.urls import path
from .views import add_transaction, spend_points, balance

urlpatterns = [
    path('add', add_transaction, name='add_transaction'),
    path('spend', spend_points, name='spend_points'),
    path('balance', balance, name='balance')
]

"""
URL patterns for the transactions app.

- add: Add a new transaction.
- spend: Spend points from the balance.
- balance: View the current balance.
"""
