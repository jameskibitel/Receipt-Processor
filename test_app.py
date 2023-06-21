#################################################################################
#  Title: test_app.py
#   
#  Description: Holds the unit tests for both Flask APIs and  all of the helper 
#  functions in app.py Run by calling 'python3 test_app.py'
#  in your terminal.
#
#################################################################################

from app import *
import unittest 
import re

class TestReceiptApis(unittest.TestCase):
    
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_process_receipt(self):
        receipt = {
                    "retailer": "Target",
                    "purchaseDate": "2022-01-01",
                    "purchaseTime": "13:01",
                    "items": [
                        {
                            "shortDescription": "Mountain Dew 12PK",
                            "price": "6.49"
                        },{
                            "shortDescription": "Emils Cheese Pizza",
                            "price": "12.25"
                        },{
                            "shortDescription": "Knorr Creamy Chicken",
                            "price": "1.26"
                        },{
                            "shortDescription": "Doritos Nacho Cheese",
                            "price": "3.35"
                        },{
                            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                            "price": "12.00"
                        }
                    ],
                    "total": "35.35"
                }

        # Make a POST request to /receipts/process
        response = self.client.post('/receipts/process', json = receipt)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('id', data)

        # Check that the id matches the regex pattern
        pattern = r'^\S+$'
        self.assertTrue(re.match(pattern, data['id']))

        # Make a request with an invalid receipt and ensure it aborts
        receipt = {
                    "retailer": "Target",
                    "purchaseDate": "2022-01-01",
                    "purchaseTime": "13:01",
                }
        
        # Make a POST request to /receipts/process
        response = self.client.post('/receipts/process', json = receipt)
        
        # Assert the response
        self.assertEqual(response.status_code, 400)

    def test_get_points(self):
        receipt = {
                    "retailer": "M&M Corner Market",
                    "purchaseDate": "2022-03-20",
                    "purchaseTime": "14:33",
                    "items": [
                        {
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        },{
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        },{
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        },{
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        }
                    ],
                    "total": "9.00"
                }

        # Make a POST request to /receipts/process
        response = self.client.post('/receipts/process', json = receipt)
        data = response.get_json()
        receipt_id = data["id"]

        # Make a GET request to /receipts/<id>/points
        response = self.client.get(f'/receipts/{receipt_id}/points')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('points', data)
        self.assertEqual(data['points'], 109)  

        # Make a request to an invalid id and ensure it aborts
        # We can assume 0 will never be a generated id since we are using uuid
        response = self.client.get(f'/receipts/0/points')

        # Assert the response
        self.assertEqual(response.status_code, 404)  

    def test_is_valid_receipt(self):
        receipt = {
                    "retailer": "Walgreens",
                    "purchaseDate": "2022-01-02",
                    "purchaseTime": "08:13",
                    "total": "2.65",
                    "items": [
                        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                        {"shortDescription": "Dasani", "price": "1.40"}
                    ]
                }
        self.assertTrue(is_valid_receipt(receipt))
        receipt = {
                    "retailer": "Target",
                    "purchaseDate": "2022-01-02",
                    "purchaseTime": "13:13",
                    "total": "1.25",
                    "items": [
                        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
                    ]
                }
        self.assertTrue(is_valid_receipt(receipt))
        receipt = {
                    "retailer": "M&M Corner Market",
                    "items": [
                        {
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        },{
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        },{
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        },{
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        }
                    ],
                    "total": "9.00"
                }
        self.assertFalse(is_valid_receipt(receipt))
        receipt = {
                    "purchaseTime": "14:33",
                    "items": [
                        {
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        },{
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        },{
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        },{
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        }
                    ],
                    "total": "9.00"
                }
        self.assertFalse(is_valid_receipt(receipt))
        receipt = {}
        self.assertFalse(is_valid_receipt(receipt))

    def test_calculate_points(self):
        receipt = {
                    "retailer": "M&M Corner Market",
                    "purchaseDate": "2022-03-20",
                    "purchaseTime": "14:33",
                    "items": [
                        {
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        },{
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        },{
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        },{
                            "shortDescription": "Gatorade",
                            "price": "2.25"
                        }
                    ],
                    "total": "9.00"
                }
        self.assertEqual(calculate_points(receipt),109) 
        receipt = {
                    "retailer": "Target",
                    "purchaseDate": "2022-01-01",
                    "purchaseTime": "13:01",
                    "items": [
                        {
                            "shortDescription": "Mountain Dew 12PK",
                            "price": "6.49"
                        },{
                            "shortDescription": "Emils Cheese Pizza",
                            "price": "12.25"
                        },{
                            "shortDescription": "Knorr Creamy Chicken",
                            "price": "1.26"
                        },{
                            "shortDescription": "Doritos Nacho Cheese",
                            "price": "3.35"
                        },{
                            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                            "price": "12.00"
                        }
                    ],
                    "total": "35.35"
                }
        self.assertEqual(calculate_points(receipt),28)
        receipt = {
                    "retailer": "Target",
                    "purchaseDate": "2022-01-02",
                    "purchaseTime": "13:13",
                    "total": "1.25",
                    "items": [
                        {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
                    ]
                }
        self.assertEqual(calculate_points(receipt),31)

    def test_count_alphanumeric(self):
        self.assertEqual(count_alphanumeric("Aldi"),4)
        self.assertEqual(count_alphanumeric("Forever 21"),9)
        self.assertEqual(count_alphanumeric("-$-$   +^& * Festival )  "),8)
        self.assertEqual(count_alphanumeric("{({8})}"),1)

    def test_is_round_dollar(self): 
        self.assertTrue(is_round_dollar("20.00"))
        self.assertTrue(is_round_dollar("9.00"))
        self.assertFalse(is_round_dollar("45.90"))
        self.assertFalse(is_round_dollar("4.99"))

    def test_is_multiple_of_quarter(self):
        self.assertTrue(is_multiple_of_quarter("450.50"))
        self.assertTrue(is_multiple_of_quarter("0.75"))
        self.assertFalse(is_multiple_of_quarter("8.90"))
        self.assertFalse(is_multiple_of_quarter("17.99"))

    def test_count_multiples_of_two(self):
         items = []
         self.assertEqual(count_multiples_of_two(items), 0) 
         items = [
            {
                "shortDescription": "Doritos",
                "price": "3.49"
            }
         ]
         self.assertEqual(count_multiples_of_two(items), 0)
         items = [
            {
                "shortDescription": "Doritos",
                "price": "3.49"
            },{
                "shortDescription": "Pizza Rolls",
                "price": "5.05"
            },{
                "shortDescription": "Almond Joy",
                "price": "1.25"
            },{
                "shortDescription": "Kit-Kat",
                "price": "1.00"
            }
         ]
         self.assertEqual(count_multiples_of_two(items), 2) 
         items = [
            {
                "shortDescription": "Doritos",
                "price": "3.49"
            },{
                "shortDescription": "Pizza Rolls",
                "price": "5.05"
            },{
                "shortDescription": "Almond Joy",
                "price": "1.25"
            }
         ]
         self.assertEqual(count_multiples_of_two(items), 1)

    def test_trimmed_item_multiple_of_three(self):
        items = []
        self.assertEqual(trimmed_item_multiple_of_three(items), 0) 
        items = [
            {
                "shortDescription": " Dorito   ",
                "price": "3.49"
            }
         ]
        self.assertEqual(trimmed_item_multiple_of_three(items), 1)
        items = [
            {
                "shortDescription": "  Nectarine  ",
                "price": "2.00"
            },{
                "shortDescription": "Pizza Rolls  ",
                "price": "5.05"
            },{
                "shortDescription": " Almond Joy ",
                "price": "1.25"
            },{
                "shortDescription": " Pineapple",
                "price": "7.54"
            }
         ]
        self.assertEqual(trimmed_item_multiple_of_three(items), 3) 
        items = [
            {
                "shortDescription": "Dorito bag",
                "price": "4.46"
            },{
                "shortDescription": "Pistachios         ",
                "price": "5.05"
            }
         ]
        self.assertEqual(trimmed_item_multiple_of_three(items), 0)

    def test_is_purchase_day_odd(self):
        self.assertTrue(is_purchase_day_odd("2023-06-21"))
        self.assertTrue(is_purchase_day_odd("2005-12-15"))
        self.assertTrue(is_purchase_day_odd("1943-01-01"))
        self.assertFalse(is_purchase_day_odd("2020-06-28"))
        self.assertFalse(is_purchase_day_odd("1974-08-18"))
        self.assertFalse(is_purchase_day_odd("1987-06-04"))

    def test_is_between_2pm_and_4pm(self):
        self.assertTrue(is_between_2pm_and_4pm("14:15"))
        self.assertTrue(is_between_2pm_and_4pm("15:45"))
        self.assertFalse(is_between_2pm_and_4pm("14:00"))
        self.assertFalse(is_between_2pm_and_4pm("16:00"))
        self.assertFalse(is_between_2pm_and_4pm("09:00"))
        self.assertFalse(is_between_2pm_and_4pm("20:00"))

if __name__ == "__main__":
    unittest.main()