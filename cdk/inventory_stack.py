from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    custom_resources as cr,
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
