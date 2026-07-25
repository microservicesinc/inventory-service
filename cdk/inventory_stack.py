from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_sqs as sqs,
    custom_resources as cr,
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_events,
    RemovalPolicy
)
from constructs import Construct

class InventoryStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Define the Single Table
        inventory_table = dynamodb.Table(
            self, "InventoryTable",
            table_name="InventoryOrdersTable",
            partition_key=dynamodb.Attribute(name="PK", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="SK", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY 
        )

        # 2. Seed Initial Test Data on Deployment
        # We invoke this helper construct to inject items sequentially using the DynamoDB API
        cr.AwsCustomResource(
            self, "SeedInventoryData",
            on_create=cr.AwsSdkCall(
                service="DynamoDB",
                action="putItem",
                parameters={
                    "TableName": inventory_table.table_name,
                    "Item": {
                        "PK": {"S": "ITEM#item1"},
                        "SK": {"S": "METADATA"},
                        "stock": {"N": "10"}
                    }
                },
                # Generates a static ID to track deployment resource states
                physical_resource_id=cr.PhysicalResourceId.of("InventoryInitialSeed")
            ),
            # Grant permission to allow the custom resource lambda to execute the table insert
            policy=cr.AwsCustomResourcePolicy.from_sdk_calls(
                resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE
            )
        )

        # Seed a second item using a separate custom resource block
        cr.AwsCustomResource(
            self, "SeedInventoryData2",
            on_create=cr.AwsSdkCall(
                service="DynamoDB",
                action="putItem",
                parameters={
                    "TableName": inventory_table.table_name,
                    "Item": {
                        "PK": {"S": "ITEM#item2"},
                        "SK": {"S": "METADATA"},
                        "stock": {"N": "5"}
                    }
                },
                physical_resource_id=cr.PhysicalResourceId.of("InventoryInitialSeed2")
            ),
            policy=cr.AwsCustomResourcePolicy.from_sdk_calls(
                resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE
            )
        )

        # 2. Define the two SQS Queues
        stock_update_queue = sqs.Queue(self, "StockUpdateQueue", queue_name="StockUpdateQueue")
        stock_query_queue = sqs.Queue(self, "StockQueryQueue", queue_name="StockQueryQueue")

        # 3. Define the SQS-triggered Lambdas (pointing to our src application directory)
        update_lambda = _lambda.Function(
            self, "UpdateStockLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset("../src"), # Relative path to your app code
            handler="lambdas.update_stock.handler",
        )

        # 4. Attach SQS Triggers to the Lambdas
        update_lambda.add_event_source(lambda_events.SqsEventSource(stock_update_queue))

        # 5. Grant Permissions (Smart Defaults!)
        inventory_table.grant_write_data(update_lambda)