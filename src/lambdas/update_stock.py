import json
import os
import boto3
from botocore.exceptions import ClientError

# Global initialization happens once when the container boots up.
# Lambda natively populates AWS settings, or reads environment overrides from CDK.
TABLE_NAME = os.getenv("DYNAMODB_TABLE", "InventoryOrdersTable")
ENDPOINT_URL = os.getenv("LOCALSTACK_ENDPOINT")  # Present only during local testing phases

# Initialize the table resource object cleanly without logic branching
db_kwargs = {"endpoint_url": ENDPOINT_URL} if ENDPOINT_URL else {}
dynamodb = boto3.resource("dynamodb", **db_kwargs)
table = dynamodb.Table(TABLE_NAME)

def handler(event, context):
    """
    AWS Lambda entrypoint triggered asynchronously by SQS queues.
    Executes atomic counter adjustments directly against the target table.
    """
    print(f"📥 Received SQS Batch Event: {json.dumps(event)}")
    
    for record in event.get('Records', []):
        try:
            # Parse individual message payload string into a JSON dictionary
            body = json.loads(record['body'])
            item_id = body.get('itemId')
            quantity_change = body.get('quantityChange')
            
            if not item_id or quantity_change is None:
                print(f"⚠️ Skipping invalid envelope: {body}")
                continue
                
            # Perform atomic increment mutation securely using an expression
            print(f"⚙️ Applying atomic stock adjustment for {item_id}: {quantity_change}")
            table.update_item(
                Key={
                    "PK": f"ITEM#{item_id}",
                    "SK": "METADATA"
                },
                UpdateExpression="SET stock = if_not_exists(stock, :start) + :change",
                ExpressionAttributeValues={
                    ":change": int(quantity_change),
                    ":start": 0
                }
            )
            print(f"✅ Stock mutation successfully committed for {item_id}")
            
        except ClientError as e:
            print(f"❌ DynamoDB transaction failure: {e.response['Error']['Message']}")
            raise e
        except Exception as e:
            print(f"❌ Internal process execution runtime fault: {str(e)}")
            raise e
            
    return {"statusCode": 200, "body": "SQS Batch events processed successfully."}
