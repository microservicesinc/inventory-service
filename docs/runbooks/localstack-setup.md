# LocalStack Docker Setup

## 1. Docker Compose Configuration (`docker-compose.yml`)

```sh
services:
  localstack:
    container_name: localstack_main
    image: localstack/localstack:latest
    ports:
      - "127.0.0.1:4566:4566"            # LocalStack Gateway
      - "127.0.0.1:4510-4559:4510-4559"  # External service port range
    environment:
      - DEBUG=${DEBUG:-0}
      - DISABLE_PRO=1
      - DOCKER_HOST=unix:///var/run/docker.sock
    volumes:
      - "${LOCALSTACK_VOLUME_DIR:-./volume}:/var/lib/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"
```

## 2. How to Run

1. Start the LocalStack container in detached mode:
   docker compose up -d

2. Check the status of the container:
   docker compose ps

3. View logs to ensure service initialization:
   docker compose logs -f localstack

4. Stop the service:
   docker compose down

## 3. Using

```sh
pip install localstack
```