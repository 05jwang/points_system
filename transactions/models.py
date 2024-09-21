from django.db import models


class Transaction(models.Model):
    """
    Represents a transaction in the points system.

    Attributes:
        payer (str): The name of the payer.
        points (int): The number of points for the transaction.
        timestamp (datetime): The timestamp of the transaction.
    """

    payer = models.CharField(max_length=100)
    points = models.IntegerField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.payer} - {self.points} points"
