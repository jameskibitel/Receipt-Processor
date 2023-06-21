#################################################################################
#  Title: app.py
#   
#  Description: Contains APIs for processing receipts and calculating 
#  points based on specific criteria. It provides two endpoints: 
#  1. "/receipts/process" - Processes the JSON receipt and returns a unique ID for the receipt.
#  2. "/receipts/<id>/points" - Retrieves the points associated with a receipt using its ID.
#  The APIs use the dictionary "receiptDict" to store the points associated with each receipt ID.
#
#################################################################################


from flask import Flask, request, jsonify, abort
import math
import uuid

app = Flask(__name__)

# Will store the 'id : points' key-value pairs in memory
receiptDict = {}

@app.route("/receipts/process", methods = ["POST"])
def process_receipt():
    """
    Description: Processes a receipt and calculates the points based on specific criteria.

    Request: JSON object representing the receipt. Contains the following fields:
            - retailer: Name of the retailer.
            - purchaseDate: Date of purchase.
            - purchaseTime: Time of purchase (military time).
            - items: List of items on the receipt. Each item contains a "shortDescription" and "price" field.
            - total: Total amount on the receipt

    Returns: JSON object containing the unique ID for the input receipt.
    """
    receipt = request.get_json()

    # If the receipt is invalid, abort
    if not is_valid_receipt(receipt):
        abort(400, "The receipt is invalid")

    generatedId = str(uuid.uuid4()) 

    # Calculate the points awarded to the receipt and put it in the dictionary
    pointTotal = calculate_points(receipt)
    receiptDict[generatedId] = pointTotal
    receiptId = {
        "id": generatedId
    }

    return jsonify(receiptId), 200
        
@app.route("/receipts/<id>/points", methods = ["GET"])
def get_points(id):
    """
    Description: Retrieves the points associated with a receipt using its ID.

    Request: Receipt ID as part of the URL path.

    Returns: JSON object containing the points associated with the receipt.
    """
    # Abort if the id doesn't exist in receiptDict
    if id not in receiptDict:
        abort(404, "No receipt found for that id")

    points = {
        "points": receiptDict[id]
    }

    return jsonify(points), 200

def is_valid_receipt(receipt):
    """
    Description: Validates the input JSON receipt

    Parameters: receipt - dictionary of the JSON received from the process_receipt API

    Returns: Boolean indicating if the receipt is valid or not
    """
    required_fields = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]

    # Loop over the required fields and check that they are in the input receipt
    for field in required_fields:
        if receipt.get(field) == None:
            return False
        
    return True

def calculate_points(receipt):
    """
    Description: Calculates the points for a receipt based on the following criteria:
    1. One point for every alphanumeric character in the retailer name.
    2. 50 points if the total is a round dollar amount with no cents.
    3. 25 points if the total is a multiple of 0.25.
    4. 5 points for every two items on the receipt.
    5. If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and 
       round up to the nearest integer. The result is the number of points earned.
    6. 6 points if the day in the purchase date is odd.
    7. 10 points if the time of purchase is after 2:00pm and before 4:00pm.

    Parameters: receipt - dictionary of the JSON received from the process_receipt API

    Returns: Integer value representing the total points awarded for the receipt.
    """
    totalPoints = 0
    
    totalPoints += count_alphanumeric(receipt["retailer"])
    
    if is_round_dollar(receipt["total"]):
        totalPoints += 50

    if is_multiple_of_quarter(receipt["total"]):
        totalPoints += 25

    totalPoints += count_multiples_of_two(receipt["items"]) * 5

    totalPoints += trimmed_item_multiple_of_three(receipt["items"])

    if is_purchase_day_odd(receipt["purchaseDate"]):
        totalPoints += 6

    if is_between_2pm_and_4pm(receipt["purchaseTime"]):
        totalPoints += 10

    return totalPoints

def count_alphanumeric(retailer):
    """
    Description: Counts the number of alphanumeric characters in the retailer name.

    Parameters: retailer - String representing the name of the retailer.

    Returns: Integer value representing the number of alphanumeric characters in the retailer name.
    """
    points = 0
    for char in retailer:
        if char.isalnum():
            points += 1
    return points

def is_round_dollar(total):
    """
    Description: Checks if the total amount on the receipt is a round dollar value.

    Parameters: total - Total amount on the receipt.

    Returns: Boolean indicating if the total is a round dollar amount or not.
    """
    return float(total) == int(float(total))

def is_multiple_of_quarter(total):
    """
    Description: Checks if the total amount on the receipt is a multiple of 0.25.

    Parameters: total - Total amount on the receipt.

    Returns: Boolean indicating if the total is a multiple of 0.25 or not.
    """
    return float(total) % 0.25 == 0

def count_multiples_of_two(items):
    """
    Description: Counts the number of items on the receipt and returns the floor division by 2.

    Parameters: items - List of items on the receipt. Each item contains a "shortDescription" and "price" field.

    Returns: Integer value representing the number of items divided by 2 (floor division).
    """
    return len(items) // 2

def trimmed_item_multiple_of_three(items):
    """
    Description: Iterates through all the items on the receipt, and calculates the 
    points for each eligible item. If the trimmed length of an item's description is a multiple of 3,  
    the points earned are the item's price multiplied by 0.2 and rounded up to the nearest integer.

    Parameters: items - List of items on the receipt. Each item contains a "shortDescription" and "price" field.

    Returns: Integer value representing the total points earned based on the length of trimmed item descriptions.
    """
    points = 0
    for i in items:
        if len(i["shortDescription"].strip()) % 3 == 0:
            points += math.ceil(float(i["price"]) * .2)
    return points

def is_purchase_day_odd(purchaseDate):
    """
    Description: Checks if the day in the purchase date was an odd number.

    Parameters: purchaseDate - Date of purchase.

    Returns: Boolean indicating if the day of the purchase date was an odd number or not.
    """
    return int(purchaseDate[-2:]) % 2 == 1

def is_between_2pm_and_4pm(purchaseTime):
    """
    Description: Checks if the purchase time was after 2 PM and before 4 PM (not inclusive) 

    Parameters: purchaseTime - Time of purchase (military time).

    Returns: Boolean indicating if the purchase time was after 2 PM and before 4 PM or not.
    """
    # Remove ":" from the time
    trimmedTime = int(purchaseTime.replace(":", ""))

    return 1400 < trimmedTime < 1600

if __name__ == "__main__":
    app.run(debug=False)
