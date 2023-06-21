# Receipt Processor

## Project Description
This project offers two Flask APIs (both built in app.py) that together can process and calculate points for a receipt. The rules by which points are awarded are

* One point for every alphanumeric character in the retailer name.
* 50 points if the total is a round dollar amount with no cents.
* 25 points if the total is a multiple of ```0.25```.
* points for every two items on the receipt.
* If the trimmed length of the item description is a multiple of 3, multiply the price by ```0.2``` and round up to the nearest integer. The result is the number of points earned.
* 6 points if the day in the purchase date is odd.
* 10 points if the time of purchase is after 2:00pm and before 4:00pm.

The project comprises two endpoints:

* ```/receipts/process``` - This endpoint processes a JSON receipt and generates a unique identifier for the receipt.
* ```/receipts/{id}/points``` - This endpoint retrieves the points assigned to a receipt based on its corresponding ID.

To manage the points and their association with each receipt ID, the APIs utilize a dictionary called "receiptDict" which stores information in memory as long as the Flask app is running.

## Installation and Setup
(these instructions assume that you have [git](https://git-scm.com/downloads) and [docker](https://www.docker.com/products/docker-desktop/) installed)
1. Clone the repo and navigate to the Receipt-Processor directory:
   ```
   git clone https://github.com/jameskibitel/Receipt-Processor
   cd Receipt-Processor
   ```
2. Build the Docker image using the following command:
   ```
   docker build -t receipt-processor-docker .
   ```
   The Dockerfile also runs the tests located in test_app.py, and will only build the 
   image if all the tests pass. You can confirm that the build worked by running 
   ```docker images``` and ensuring that you see receipt-processor-docker listed. 
   
3. Run a Docker container based on the image you built using the following command:
   ```
   docker run -p 5000:5000 receipt-processor-docker
   ```
   In the terminal, you should see an output similar to the following:
   ```console
   * Debug mode: off
   WARNING: This is a development server. Do not use it in a production deployment. Use 
   a production WSGI server instead.
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:5000
   * Running on http://172.17.0.2:5000
   Press CTRL+C to quit
   ```
   
4. The Flask app should now be accessible. If you are running the Docker container 
   locally, you can use ```http://127.0.0.1:5000``` (or whatever follows 
   the first ```* Running on http:``` from the terminal output).

## API Endpoints
### Process Receipt
* URL: ```/receipts/process```
* Method: ```POST```
* Description: Processes a receipt and calculates the points based on the criteria 
  mentioned above.
* Payload: JSON object representing a valid receipt.
* Response: JSON object containing the unique ID for the input receipt.

### Get Points
* URL: ```/receipts/{id}/points```
* Method: ```GET```
* Description: Retrieves the points associated with a receipt using its ID.
* Path Parameters: {id} - The ID of the receipt to retrieve the points for.
* Response: JSON object containing the points awarded to the receipt.

## Usage
To use the project, follow these steps:

1. Make sure the Flask app is running.

2. Send a POST request to the ```/receipts/process``` endpoint with a JSON object 
   representing the receipt. A receipt will only be valid if it includes the retailer 
   name, purchase date, purchase time, items, and total amount. 
   
4. The API will process the receipt, calculate the points for it, and return a JSON 
   object holding the unique ID for the receipt.
   ```YAML
   {
       "id": "44f39c89-39cf-4c2b-9cb5-433fd0917cc4"
   }
   ```

5. Retrieve the points associated with a receipt by sending a GET request to the 
   ```/receipts/{id}/points``` endpoint, where {id} is the ID of the receipt you want to 
   retrieve the points for.

6. The API will return a JSON object holding the points that receipt was rewarded.
   ```YAML
   {
       "points": 15
   }
   ```
   
   
