# Inventory Microservice - Local Development Runbook

This guide outlines the step-by-step chronological workflow to spin up infrastructure using AWS CDK, launch the Flask API locally via LocalStack, and test endpoints using the Swagger UI.

---

## 📋 Prerequisites

Ensure you have the following global CLI utilities installed on your host machine:
* **Docker & Docker Compose**
* **Node.js** (for CDK utilities)
* **Python 3.11+**

```bash
# Install the necessary global AWS CDK Local tools
npm install -g aws-cdk-local aws-cdk
```

---

## 🚀 Chronological Execution Steps

### Step 1: Start the LocalStack Container
Launch the background Docker containers to emulate core AWS capabilities (DynamoDB and SQS) locally.
```bash
docker compose up -d
```

### Step 2: Bootstrap the Local CDK Environment
Initialize the local container environment with the necessary tracking parameters and staging buckets required by AWS CDK. *(Required only on the very first run).*
```bash
cd cdk
cdklocal bootstrap
```

### Step 3: Deploy Infrastructure via CDK
Compile your Python CDK stack definitions and provision the `InventoryOrdersTable` inside LocalStack.
```bash
cdklocal deploy --require-approval never
cd ..
```

### Step 4: Install Python Dependencies
Set up your local python runtime environment or activate your virtual environment, then pull down application package mirrors.
```bash
pip install -r requirements.txt
```

### Step 5: Launch the Flask API Application
Execute the root wrapper code script to launch your microservice execution layers on your local host.
```bash
python app.py
```

---

## 🧪 Verification and Testing

### 1. Interactive Documentation (Swagger UI)
Once the server boots up successfully, open your browser and navigate to:
👉 **[http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)**

### 2. Manual CLI Table Verification
To guarantee that AWS CDK created your target physical tables perfectly inside LocalStack, open a separate terminal and run:
```bash
# Expected output includes: "InventoryOrdersTable"
aws dynamodb list-tables --endpoint-url http://localhost:4566 --region us-east-1
```

### 3. Clean Infrastructure Teardown
To wipe out infrastructure assets and reset your local data tables to a clean slate, terminate your runtime threads and execute:
```bash
# Destroy CDK resources
cd cdk && cdklocal destroy --force && cd ..

# Stop active docker containers
docker compose down -v
```
