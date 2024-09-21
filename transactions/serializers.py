from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.

    Serializes the Transaction model fields: payer, points, and timestamp.
    """
    class Meta:
        model = Transaction
        fields = ['payer', 'points', 'timestamp']
