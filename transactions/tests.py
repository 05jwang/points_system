from django.test import TestCase
from rest_framework.test import APIClient
from .models import Transaction


class TransactionTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        Transaction.objects.all().delete()

    def test_add_transaction(self):
        """
        Test case for adding transactions.

        This test case verifies that transactions can be added successfully and that the transactions are spent in the correct order.

        Steps:
        1. Create a list of transactions with payer, points, and timestamp.
        2. Iterate over each transaction and send a POST request to '/add' endpoint with the transaction data.
        3. Verify that the response status code is 200 for each transaction.
        4. Send a GET request to '/balance' endpoint and verify that the response status code is 200.
        5. Verify that the response content matches the expected balance.
        6. Send a POST request to '/spend' endpoint with the points to spend.
        7. Verify that the response status code is 200.
        8. Send a GET request to '/balance' endpoint and verify that the response status code is 200.
        9. Verify that the response content matches the expected balance after spending.

        """
        # Add transactions
        transactions = [
            {"payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z"},
            {"payer": "UNILEVER", "points": 200,
                "timestamp": "2022-10-31T11:00:00Z"},
            {"payer": "DANNON", "points": -200,
                "timestamp": "2022-10-31T15:00:00Z"},
            {"payer": "DANNON", "points": 1000,
                "timestamp": "2022-11-02T14:00:00Z"},
            {"payer": "MILLER COORS", "points": 10000,
                "timestamp": "2022-11-01T14:00:00Z"},
        ]
        for transaction in transactions:
            response = self.client.post('/add', transaction, format='json')
            self.assertEqual(response.status_code, 200)

        # Check balance before spending
        response = self.client.get('/balance')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "DANNON": 1100,
            "MILLER COORS": 10000,
            "UNILEVER": 200
        })

        # Spend points
        response = self.client.post('/spend', {"points": 5000}, format='json')
        self.assertEqual(response.status_code, 200)

        # Check balance after spending
        response = self.client.get('/balance')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "DANNON": 1000,
            "MILLER COORS": 5300,
            "UNILEVER": 0
        })

    def test_spend_points_invalid_points(self):
        """
        Test case to verify the behavior when spending points with invalid points value.

        It sends POST requests to '/spend' endpoint with invalid points value and checks if the response
        status code is 400 (Bad Request) and the response data contains the expected error message.
        """

        # Not enough points
        response = self.client.post('/spend', {"points": 500}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "Not enough points")

        # Invalid points value
        response = self.client.post('/spend', {"points": -1}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, "Invalid points value")

    def test_add_transaction_invalid_data(self):
        """
        Test case to verify the behavior when adding a transaction with invalid data.

        It sends POST requests to '/add' endpoint with invalid data and checks if the response
        status code is 400 (Bad Request) and the response data contains the expected error message.

        """

        # Missing a field (timestamp)
        response = self.client.post(
            '/add', {"payer": "DANNON", "points": 300}, format='json')

        self.assertEqual(response.status_code, 400)

        # Invalid timestamp format
        response = self.client.post(
            '/add', {"payer": "DANNON", "points": 100, "timestamp": "2022-1031T10:00:00"}, format='json')
        self.assertEqual(response.status_code, 400)
