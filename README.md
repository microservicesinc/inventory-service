# inventory-service
Service for inventory management

## Project Idea
The Inventory Service is a microservice designed to manage product stock levels in real-time. It provides an API to track, update, and query inventory items, ensuring data consistency across distributed systems. It also includes an AWS Lambda function to synchronize inventory updates via SQS.

## Components
- **Flask**: The core web framework used to build the RESTful API.
- **DynamoDB**: The NoSQL database used for storing inventory data.
- **Localstack**: Used for local development and testing of AWS services (DynamoDB, SQS).
- **Swagger/OpenAPI**: Integrated for API documentation and testing.
- **AWS Lambda**: Handles asynchronous inventory synchronization triggered by SQS.
- **Pytest**: Framework for unit and integration testing.

## Running the Flask API
To run the Flask API locally, follow these steps:

1. Ensure you have your virtual environment activated.
2. Install the dependencies: `pip install -r requirements.txt`
3. Set the `FLASK_APP` environment variable: `export FLASK_APP=src/api/main.py`
4. Run the application: `flask run`

## API Documentation
Once the application is running, you can access the Swagger UI documentation at:
`http://localhost:5000/apidocs`

## Development
- Ensure you follow the conventions outlined in `CONVENTIONS.md`.
- Use `pytest` to run tests.
