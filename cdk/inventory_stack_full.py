from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_events,
    RemovalPolicy
)
from constructs import Construct

class InventoryStackFull(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Define the Single DynamoDB Table
        inventory_table = dynamodb.Table(
            self, "InventoryTable",
            table_name="InventoryOrdersTable",
            partition_key=dynamodb.Attribute(name="PK", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="SK", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            # Destroys table data during local testing teardowns. Change to RETAIN for actual prod stacks.
            removal_policy=RemovalPolicy.DESTROY 
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

        query_lambda = _lambda.Function(
            self, "QueryStockLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset("../src"),
            handler="lambdas.query_stock.handler",
        )

        # 4. Attach SQS Triggers to the Lambdas
        update_lambda.add_event_source(lambda_events.SqsEventSource(stock_update_queue))
        query_lambda.add_event_source(lambda_events.SqsEventSource(stock_query_queue))

        # 5. Grant Permissions (Smart Defaults!)
        inventory_table.grant_write_data(update_lambda)
        inventory_table.grant_read_data(query_lambda)
