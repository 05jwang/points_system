from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
from collections import defaultdict
from django.db.models import Sum
from django.http import JsonResponse


@api_view(['POST'])
def add_transaction(request):
    """
    Add a new transaction.

    Parameters:
    - request: The HTTP request object containing the transaction data.

    Returns:
    - If the transaction data is valid, returns a HTTP 200 Created response with no body.
    - If the transaction data is invalid, returns a HTTP 400 Bad Request response with the serializer errors.
    """
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def spend_points(request):
    """
    API endpoint for spending points. Spends the points by timestamp (oldest first).

    Parameters:
        request (Request): The HTTP request object.

    Returns:
        Response: The HTTP response object containing a list of points deducted from each payer.

    Raises:
        HTTP 400 Bad Request: If the points value is invalid or not enough points are available.
    """
    points_to_spend = int(request.data.get('points'))

    # Validate points value
    if not points_to_spend or points_to_spend <= 0:
        return Response("Invalid points value", status=status.HTTP_400_BAD_REQUEST)

    # Check if there are enough points to spend
    total_points = Transaction.objects.aggregate(Sum('points'))[
        'points__sum'] or 0
    if points_to_spend > total_points:
        return Response("Not enough points", status=status.HTTP_400_BAD_REQUEST)

    # Spend points by timestamp (oldest first)
    transactions = Transaction.objects.order_by('timestamp')
    spent_points = defaultdict(int)
    remaining_points = points_to_spend

    for transaction in transactions:
        if remaining_points <= 0:
            break

        points_to_deduct = min(transaction.points, remaining_points)
        spent_points[transaction.payer] -= points_to_deduct
        transaction.points -= points_to_deduct
        transaction.save()
        remaining_points -= points_to_deduct

    return Response([{"payer": payer, "points": points} for payer, points in spent_points.items()], status=status.HTTP_200_OK)


@api_view(['GET'])
def balance(request):
    """
    Retrieve the balance of points for each payer.

    This function aggregates the points by payer from the Transaction model
    and returns a dictionary containing the payer as the key and the total
    points as the value.

    Parameters:
    - request: The HTTP request object containing the transaction data.
    Returns:
        Response: A Response object containing the balance dictionary.
    """
    balances = Transaction.objects.values('payer').annotate(
        total_points=Sum('points')).order_by('payer')
    return Response({balance['payer']: balance['total_points'] for balance in balances}, status=status.HTTP_200_OK)
