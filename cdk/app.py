import aws_cdk as cdk
from inventory_stack import InventoryStack

app = cdk.App()
InventoryStack(app, "InventoryServiceStack")
app.synth()
