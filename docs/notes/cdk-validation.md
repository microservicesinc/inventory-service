# 🛠️ AWS CDK Validation Cheat Sheet

AWS CDK utilizes the validation phase to catch structural mistakes, security violations, and live AWS account state conflicts **before** deploying infrastructure.

---

### 💡 How It Works
When you validate or synthesize your code, CDK checks your infrastructure across three defense layers:
1. **Construct Validation:** Catches misconfigured code properties locally during compile time.
2. **Offline Rule Validation:** Evaluates the synthesized CloudFormation template against compliance frameworks (like `cdk-nag` or AWS Guard) without hitting AWS.
3. **Online Pre-flight Checking:** Contacts your active AWS account to verify that resource names do not already exist and service quotas are not exceeded.

---

### 💻 Essential CLI Commands

```bash
# 1. Run full online and offline validation checks against your active AWS profile
cdk validate

# 2. Run pure offline validation (Ideal for local testing or isolated CI/CD pipelines)
cdk validate --no-online

# 3. Bypass the validation phase to force a fast deployment (Development environments only)
cdk deploy --disable-validation
```

---

### 🐍 Registering Validation Plugins in Python (`app.py`)

You can register third-party guardrails directly inside your main app entry point to enforce security standards automatically:

```python
import aws_cdk as cdk
from my_stack import MyServerlessStack
# Example using the AWS CloudFormation Guard plugin
from aws_cdk.cloudformation_guard_validator import CfnGuardValidator 

app = cdk.App(
    # Attaches structural compliance validation to run instantly after synthesis
    policy_validation_beta_1=[
        CfnGuardValidator()
    ]
)

MyServerlessStack(app, "ProductionServerlessBackend")

app.synth()
```

### Cdk json configuring

The cdk.json file controls validation behavior through two main configuration blocks: context keys (which toggle formatting and validation modes) and plugin arrays (which register external compliance engines).

While running cdk validate, the configuration inside your cdk.json file dictates whether those validation reports print to your terminal or drop cleanly as a raw database object into your deployment pipeline.Here is exactly how cdk.json is structured to control validation:

```json
{
  "app": "python3 app.py",
  "plugin": [
    "custom-validation-plugin-module"
  ],
  "context": {
    "// 1. Validation Report Format Selection": "",
    "@aws-cdk/core:validationReportJson": true,

    "// 2. Strict / Warning Mode Feature Flags": "",
    "@aws-cdk/core:validationDefaultSeverity": "ERROR",

    "// 3. Historical Request Validation Flags (Resource Level)": "",
    "@aws-cdk/aws-apigateway:requestValidatorUniqueId": true
  }
}

```