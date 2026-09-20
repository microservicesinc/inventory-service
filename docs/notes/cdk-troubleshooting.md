### Troubleshooting

*  **If a cdk deploy fails...**

> Go directly to the AWS CloudFormation Console, click on your specific Stack, and navigate to the Events tab. Filter or look for the earliest red CREATE_FAILED or UPDATE_FAILED status.

* **UPDATE_ROLLBACK_FAILED**

>If a deployment fails midway, CloudFormation automatically reverses changes to return to the last known stable state. If it encounters a resource configuration issue during that rollback phase, the stack locks. Resolving this requires using the console to manually choose "Continue Update Rollback" and marking the specific problematic resource to be skipped.

* **The 1-Hour Lambda Timeout** 

>If an L3 Custom Resource fails to respond or crashes, CloudFormation waits for a confirmation token. If your custom code lacks proper error-handling catches, the stack can remain stuck in an IN_PROGRESS state for over an hour before timing out.

* **State Deletion Behaviors**

> To force Terraform-like complete removal behaviors, you must explicitly declare the removal configuration properties on stateful components with **RemovalPolicy**

```python
from aws_cdk import RemovalPolicy

table = dynamodb.Table(
    self, "MyTable",
    partition_key=...,
    # Tells CloudFormation it is safe to completely wipe this data asset on destroy
    removal_policy=RemovalPolicy.DESTROY 
)
```