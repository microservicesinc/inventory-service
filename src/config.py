import os
from dotenv import load_dotenv

# Explicitly pull configurations from your root .env workspace
load_dotenv()

class Config:
    """Centralizes application parameters and connection overrides."""
    STAGE = os.getenv("STAGE", "local")
    TABLE_NAME = os.getenv("DYNAMODB_TABLE", "InventoryOrdersTable")
    LOCALSTACK_ENDPOINT = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
    AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

    @classmethod
    def get_boto3_kwargs(cls) -> dict:
        """Computes runtime properties to inject into boto3 resource definitions."""
        kwargs = {}
        
        # Divert data connections to LocalStack container structures when operating locally
        if cls.STAGE == "local":
            kwargs["endpoint_url"] = cls.LOCALSTACK_ENDPOINT
            kwargs["region_name"] = cls.AWS_REGION
            kwargs["aws_access_key_id"] = "mock_key"
            kwargs["aws_secret_access_key"] = "mock_secret"
            
        return kwargs
