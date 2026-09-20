# 📂 AWS CDK: The `cdk.json` File Quick Reference

The **`cdk.json`** file resides at the root of your project directory. It is a configuration file that tells the CDK CLI **how to execute your code application** and **what feature flags or validation rules to apply** during synthesis and deployment.

---

### 🎛️ Standard Serverless Structure (`cdk.json`)

```json
{
  "app": "python3 app.py",
  "watch": {
    "include": [
      "**"
    ],
    "exclude": [
      "README.md",
      "cdk.out",
      "requirements.txt"
    ]
  },
  "context": {
    "@aws-cdk/aws-apigateway:usagePlanKeyOrderInsensitive": true,
    "@aws-cdk/core:stackRelativeExports": true,
    "@aws-cdk/aws-lambda:recognizeVersionProps": true,
    "environment": "production",
    "billing_code": "finance-101"
  }
}
```

---

### 🔍 Core Configuration Components Explained

#### 1. The `"app"` Directive (The Execution Hook)
* **What it does:** Defines the exact CLI entrypoint shell command that CDK executes when you run commands like `cdk synth`, `cdk validate`, or `cdk deploy`.
* **Terraform Equivalent:** This is equivalent to configuring your workspace environment variables or provider blocks. It tells the execution engine which runtime compiler (e.g., Python, Node.js) to initialize.

#### 2. The `"watch"` Directive (Hot-Swapping Development)
* **What it does:** Works alongside the `cdk watch` execution loop. It tracks changes to files within your workspace directory. When you modify your application Lambda code files inside your source folder, it instantly hot-swaps the code live in AWS without triggering a full CloudFormation stack update.

#### 3. The `"context"` Key (Feature Flags & Custom Variables)
* **Feature Flags (`@aws-cdk/...`):** These strings are automatically populated by AWS when you run `cdk init`. They ensure your app utilizes the latest modern security and deployment behavioral defaults without breaking older existing architectures.
* **Custom User Variables:** You can drop custom static constants into this block (e.g., `"environment": "production"`). You can cleanly extract these inside your Python files using the native context reader method:
  ```python
  current_env = self.node.try_get_context("environment")
  ```


## Environments

To dynamically switch between **Development** and **Production** environments context keys is used, mapping them directly into your stack.

---

### 1. Update your `cdk.json` Context
Add your environment-specific configurations directly inside the `"context"` block of your `cdk.json` file:

```json
{
  "app": "python3 app.py",
  "context": {
    "environments": {
      "dev": {
        "queue_name": "StockUpdateQueue-Dev",
        "lambda_memory": 128
      },
      "prod": {
        "queue_name": "StockUpdateQueue-Prod",
        "lambda_memory": 1024
      }
    }
  }
}
```

---

### 2. Read Context in your Python Stack (`stack.py`)
Use `self.node.try_get_context` to pull the active environment configuration into your resources seamlessly:

```python
from aws_cdk import (
    Stack,
    aws_sqs as sqs,
    aws_lambda as _lambda
)
from constructs import Construct

class MyServerlessStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, target_env: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Fetch the environments dictionary from cdk.json
        all_envs = self.node.try_get_context("environments")
        
        # 2. Extract configuration specific to our target environment
        env_config = all_envs.get(target_env)

        # 3. Apply configurations dynamically to your Level 2 constructs
        stock_update_queue = sqs.Queue(
            self, "StockUpdateQueue", 
            queue_name=env_config["queue_name"]
        )

        update_lambda = _lambda.Function(
            self, "UpdateStockLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset("../src"),
            handler="lambdas.update_stock.handler",
            memory_size=env_config["lambda_memory"]
        )
```

---

### 3. Route the Environment in your Entrypoint (`app.py`)
Pass the environment flag from your CLI execution directly into your stack initialization loop:

```python
import aws_cdk as cdk
from stack import MyServerlessStack

app = cdk.App()

# Read the runtime context variable passed via CLI (e.g., -c env=dev)
env_flag = app.node.try_get_context("env") or "dev"

# Instantiate your stack with the specific target configuration parameters
MyServerlessStack(
    app, f"ServerlessBackend-{env_flag.capitalize()}",
    target_env=env_flag
)

app.synth()
```

---

### 💻 How to Deploy Each Workspace Environment
Similar to targeting workspaces in Terraform, you pass a simple **context parameter `-c` flag** directly to your CLI deployment triggers:

```bash
# Deploy to the development stack
cdk deploy -c env=dev

# Deploy to the production stack
cdk deploy -c env=prod
```
