# Project Conventions

1. All code must be documented with JSDoc comments.
2. Use camelCase for variable and function names.
3. Always use strict equality (===) instead of loose equality (==).
4. Keep functions small and focused on a single responsibility.
5. Commit messages should follow the Conventional Commits specification.
6. Flask Microservice Guidelines:
    - Use Flask for the web framework.
    - Use `boto3` for DynamoDB interactions.
    - Configure `boto3` to point to the Localstack endpoint when running in local environments (use environment variables to toggle endpoints).
    - Use `flasgger` or `flask-restx` to implement Swagger/OpenAPI documentation.
    - Ensure all API endpoints are documented with Swagger schemas.
7. AWS Lambda Guidelines:
    - Keep Lambda functions lightweight; delegate business logic to shared service modules.
    - Use environment variables for configuration (e.g., SQS queue URLs, DynamoDB table names).
8. Testing Guidelines:
    - Use `pytest` for all testing.
    - Place tests in the `tests/` directory mirroring the `src/` structure.
    - Use `pytest-mock` for mocking AWS services (DynamoDB/SQS) where appropriate.
