# 🏗️ AWS CDK: Construct Levels (L1, L2, L3) Cheat Sheet

The AWS CDK categorizes infrastructure components into three distinct tiers called **Construct Levels**. Understanding these layers helps you choose between granular configuration control and automated developer architectures.

---

### 🗂️ The Three Construct Levels Matrix

| Level | Name / CDK Group | Concept | Terraform Analogy | When to Use It |
| :--- | :--- | :--- | :--- | :--- |
| **🟩 L1** | **Cfn** Resources<br>*(e.g., `CfnQueue`)* | Raw CloudFormation mapping.<br>Zero abstractions or defaults. | Raw resource declarations.<br>*(e.g., `resource "aws_sqs_queue"`)* | When a new AWS feature isn't supported by higher levels yet. |
| **🟦 L2** | **Standard** Constructs<br>*(e.g., `sqs.Queue`)* | High-level boilerplate automation.<br>Configures secure IAM and assets. | Community standard wrapper modules with embedded safe defaults. | **Your primary daily choice** for standard serverless resources. |
| **🟪 L3** | **Patterns** Frameworks<br>*(e.g., `cr.Provider`)* | Full multi-resource setups.<br>Orchestrates micro-architectures. | Highly opinionated complex modules.<br>*(e.g., automated EKS clusters)* | Custom lifecycle actions, code compilers, or third-party tooling. |

---

### 🐍 Python Implementation Differences

#### 🟩 L1 (Level 1) — Granular & Explicit
You have to manually pass every single property shape, create execution roles from scratch, and understand the raw CloudFormation specifications.
```python
from aws_cdk import aws_lambda as lambda_

# Direct mapping to AWS::Lambda::Function
lambda_.CfnFunction(
    self, "MyL1Lambda",
    runtime="python3.11",
    handler="index.handler",
    role="arn:aws:iam::123456789012:role/ManualExecutionRole", # Must be passed explicitly
    code=lambda_.CfnFunction.CodeProperty(
        zip_file="def handler(event, context): return 'Hello'"
    )
)
```

#### 🟦 L2 (Level 2) — Smart Defaults (Recommended)
CDK handles the heavy lifting. It creates the execution roles automatically, uploads local directory code to S3 seamlessly, and exposes friendly wrapper methods for configurations.
```python
from aws_cdk import aws_lambda as lambda_

# Standard CDK Construct: Implicitly handles asset packaging and IAM roles
my_lambda = lambda_.Function(
    self, "MyL2Lambda",
    runtime=lambda_.Runtime.PYTHON_3_11,
    handler="index.handler",
    code=lambda_.Code.from_asset("../src") # Automatically zips and uploads directory
)
```

#### 🟪 L3 (Level 3) — Architectural Patterns
Bridges multi-resource tasks. For instance, the L3 Python wrapper below automatically spins up an ephemeral Docker container behind the scenes to run `pip install` on external dependencies before bundling your code package.
```python
# Found in specialized sub-modules (e.g., aws_lambda_python_alpha)
from aws_cdk import aws_lambda_python_alpha as lambda_python
from aws_cdk import aws_lambda as lambda_

# Complete infrastructure pattern that builds third-party dependencies natively
lambda_python.PythonFunction(
    self, "MyL3Lambda",
    entry="my_python_app", # Looks for requirements.txt and compiles it automatically
    runtime=lambda_.Runtime.PYTHON_3_11
)
```
