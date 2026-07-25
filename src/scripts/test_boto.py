import os
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Extract variables (AWS_ENDPOINT_URL will be None if not defined in .env)
endpoint_url = os.getenv("AWS_ENDPOINT_URL") or None
region_name = os.getenv("AWS_REGION", "us-east-1")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# Initialize DynamoDB Resource
# If endpoint_url is None, boto3 defaults to real AWS endpoints.
#dynamodb = boto3.resource(
#    'dynamodb',
#    endpoint_url=endpoint_url,
#    region_name=region_name,
#    aws_access_key_id=aws_access_key_id,
#    aws_secret_access_key=aws_secret_access_key
#)

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url=os.getenv("AWS_ENDPOINT_URL") or None
)

# Example usage
table = dynamodb.Table('Orders')
print(f"Connected to DynamoDB via: {endpoint_url if endpoint_url else 'AWS Cloud'}")

# --- OPTIONAL: Add sample data for testing ---
def seed_sample_data():
    sample_orders = [
        {'OrderId': 'ORD-001', 'Customer': 'Alice', 'Total': 120, 'Status': 'COMPLETED'},
        {'OrderId': 'ORD-002', 'Customer': 'Bob', 'Total': 45, 'Status': 'PENDING'},
        {'OrderId': 'ORD-003', 'Customer': 'Charlie', 'Total': 310, 'Status': 'COMPLETED'}
    ]
    for order in sample_orders:
        table.put_item(Item=order)
    print("Sample records inserted.\n")

if __name__ == '__main__':
    # Insert test data
    seed_sample_data()

    # Read a specific record
    #get_order_by_id('ORD-001')

    # Read all records
    #get_all_orders()