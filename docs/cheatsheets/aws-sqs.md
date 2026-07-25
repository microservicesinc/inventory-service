# AWS SQS CLI Cheatsheet

### 1. Queue Management
# Create a standard queue
```sh
aws sqs create-queue --queue-name MyQueue
```

# Create a FIFO queue (requires .fifo suffix and ContentBasedDeduplication)
```sh
aws sqs create-queue --queue-name MyQueue.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true
```

# List all queues
```sh
aws sqs list-queues
```

# Get a queue URL by its name
```sh
aws sqs get-queue-url --queue-name MyQueue
```

# Delete a queue
```sh
aws sqs delete-queue --queue-url https://amazonaws.com
```

---

### 2. Message Operations
# Send a standard message
```sh
aws sqs send-message --queue-url https://amazonaws.com --message-body "Hello World"
```

# Send a FIFO message (requires MessageGroupId)
```sh
aws sqs send-message --queue-url https://amazonaws.com.fifo --message-body "FIFO Payload" --message-group-id "Group1"
```

# Receive messages (Max limit per API call is 10)
```sh
aws sqs receive-message --queue-url https://amazonaws.com --max-number-of-messages 10
```

# Receive messages with a specific Visibility Timeout (e.g., 60 seconds)
```sh
aws sqs receive-message --queue-url https://amazonaws.com --visibility-timeout 60
```

# Delete a message (Requires ReceiptHandle from receive-message output)
```sh
aws sqs delete-message --queue-url https://amazonaws.com --receipt-handle "ReceiptHandleStringExample..."
```

# Purge all messages in a queue (Removes everything permanently)
```sh
aws sqs purge-queue --queue-url https://amazonaws.com
```

---

### 3. Monitoring & Inspection
# Get count of messages waiting in the queue
```sh
aws sqs get-queue-attributes --queue-url https://amazonaws.com --attribute-names ApproximateNumberOfMessages
```

# Get count of messages hidden (currently in flight / being processed)
```sh
aws sqs get-queue-attributes --queue-url https://amazonaws.com --attribute-names ApproximateNumberOfMessagesNotVisible
```

# Get all queue metadata (DeadLetterTargetArn, Policy, Timeout, etc.)
```sh
aws sqs get-queue-attributes --queue-url https://amazonaws.com --attribute-names All
```
