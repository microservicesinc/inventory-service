# Runbook: Centralizing LocalStack Engine to Organization Infrastructure

- **Date**: 2026-07-26
- **Action**: Centralized local AWS cloud infrastructure simulator
- **Target Repository**: `org-infrastructure-repo`
- **Methodology**: Decentralized CDK Code (Service Repos) targeting a Shared Local Service Utility (Infra Repo)

---

## 🛠️ Step 1: Migrate LocalStack Components via rsync
To maintain complete integrity of the Docker files, volume setups, and initialization configurations, migrate the local development folder out of the isolated service layout into the centralized organization tree.

```bash
# Execute structural copy with progress indicators
rsync -avz --progress \
  /home/cristian/repos/microservicesinc/inventory-service/localstack/ \
  /home/cristian/repos/microservicesinc/org-infrastructure/local-dev/
```

---

## 🏗️ Step 2: Establish the Centralized Local Engine Configuration
The base `docker-compose.yml` file now resides in the shared repository space. It exposes port `4566` globally to the host computer using a dedicated, named local bridge network.

```yaml
# org-infrastructure/local-dev/docker-compose.yml
version: '3.8'

services:
  localstack:
    container_name: localstack_main
    image: localstack/localstack:latest
    ports:
      - "4566:4566"
    environment:
      - SERVICES=dynamodb,s3,sqs,sns
      - PERSISTENCE=1
    volumes:
      - localstack_data:/var/lib/localstack
    networks:
      - dev_cloud_network

volumes:
  localstack_data:

networks:
  dev_cloud_network:
    name: dev_cloud_network
    driver: bridge
```

---

## 🚀 Step 3: Global Startup Workflow
Engineers initialize the local cloud simulator only **once** per working day before starting independent application development inside individual service repositories.

```bash
# Navigate to the centralized infrastructure workspace
cd /home/cristian/repos/microservicesinc/org-infrastructure/local-dev/

# Boot up the local cloud instance in detached background mode
docker compose up -d
```

---

## 💻 Step 4: Independent Service Deployment (`cdklocal`)
With the central engine running, developers shift back into individual decoupled code repositories (`orders-service`, `inventory-service`) to deploy their standalone .NET CDK database structures natively.

```bash
# 1. Install the official LocalStack CDK wrapper utility globally
npm install -g aws-cdk-local aws-cdk

# 2. Deploy your microservice infrastructure straight to port 4566
cd /home/cristian/repos/microservicesinc/orders-service/cdk
cdklocal deploy
```

---

## ✅ Architectural Verification
- **Isolation Preserved**: Code definitions remain isolated inside each microservice workspace.
- **Port Clashes Prevented**: No duplicate container instance definitions on port `4566`.
- **Clean Execution Logs**: Applications use `appsettings.Development.json` targeting `http://localhost:4566` natively.
