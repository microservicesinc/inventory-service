import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load local .env file variables if developing outside Docker
load_dotenv()

# 1. Environment Configurations
STAGE = os.getenv("STAGE", "local")  # Fallback to local development
TABLE_NAME = os.getenv("DYNAMODB_TABLE", "InventoryOrdersTable")
LOCALSTACK_ENDPOINT = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")

def _initialize_dynamodb_resource():
    """
    Configures connection configurations based on execution stage context.
    Safely routes to LocalStack during local developer sandbox phases.
    """
    kwargs = {}
    
    if STAGE == "local":
        kwargs["endpoint_url"] = LOCALSTACK_ENDPOINT
        kwargs["region_name"] = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        kwargs["aws_access_key_id"] = "mock_key"
        kwargs["aws_secret_access_key"] = "mock_secret"
        
    return boto3.resource("dynamodb", **kwargs)

# 2. Connection Initialization
dynamodb = _initialize_dynamodb_resource()
table = dynamodb.Table(TABLE_NAME)


# 3. Core Database Operations
def update_stock_atomic(item_id: str, quantity_change: int) -> dict:
    """
    Updates stock levels using an Atomic Counter expression.
    Prevents race conditions between concurrent SQS message executions.
    """
    try:
        response = table.update_item(
            Key={
                "PK": f"ITEM#{item_id}",
                "SK": "METADATA"
            },
            # Adds quantity_change directly to existing stock. If it doesn't exist, starts at 0.
            UpdateExpression="SET stock = if_not_exists(stock, :start) + :change",
            ExpressionAttributeValues={
                ":change": quantity_change,
                ":start": 0
            },
            ReturnValues="UPDATED_NEW"
        )
        return response.get("Attributes", {})
        
    except ClientError as e:
        print(f"Error performing atomic stock update: {e.response['Error']['Message']}")
        raise e


def get_stock_balance(item_id: str) -> dict:
    """
    Fetches the item metadata to inspect active inventory balance.
    Invoked by synchronous Flask route checks or query SQS Lambdas.
    """
    try:
        response = table.get_item(
            Key={
                "PK": f"ITEM#{item_id}",
                "SK": "METADATA"
            }
        )
        # Returns item attributes or empty values dictionary if item is completely absent
        return response.get("Item", {"PK": f"ITEM#{item_id}", "stock": 0})
        
    except ClientError as e:
        print(f"Error reading item table entry: {e.response['Error']['Message']}")
        raise e

def scan_all_inventory() -> list:
    """Scans the DynamoDB table to retrieve all inventory items."""
    try:
        response = table.scan()
        items = response.get("Items", [])
        
        # Clean up the output structure to match your existing API model
        formatted_items = []
        for item in items:
            # Only process inventory metadata items
            if item.get("SK") == "METADATA":
                formatted_items.append({
                    "itemId": item["PK"].replace("ITEM#", ""),
                    "quantity": int(item.get("stock", 0))
                })
        return formatted_items
    except ClientError as e:
        print(f"Error scanning table: {e.response['Error']['Message']}")
        raise e
