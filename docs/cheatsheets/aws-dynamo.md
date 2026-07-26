# 1. Create a table (with a partition key 'userId')
aws dynamodb create-table \
    --table-name AppUsers \
    --attribute-definitions AttributeName=userId,AttributeType=S \
    --key-schema AttributeName=userId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

# 2. Describe table (check status, schema, and metadata)
aws dynamodb describe-table \
    --table-name AppUsers

# 3. Put item (insert or overwrite a single record)
aws dynamodb put-item \
    --table-name AppUsers \
    --item '{"userId": {"S": "u001"}, "name": {"S": "Bob"}, "active": {"BOOL": true}}'

# 4. Get item (retrieve a single record using the primary key)
aws dynamodb get-item \
    --table-name AppUsers \
    --key '{"userId": {"S": "u001"}}'

# 5. List items using Scan (reads entire table - use carefully)
aws dynamodb scan \
    --table-name AppUsers

# 6. Delete table (removes the table and all its data)
aws dynamodb delete-table \
    --table-name AppUsers

# ==========================================
# BONUS: Daily Development Survival Commands
# ==========================================

# List all tables in your current region
aws dynamodb list-tables

# Query items (much more efficient than Scan; searches by primary key)
aws dynamodb query \
    --table-name AppUsers \
    --key-condition-expression "userId = :id" \
    --expression-attribute-values '{":id": {"S": "u001"}}'

# Update a specific item attribute without overwriting the whole record
aws dynamodb update-item \
    --table-name AppUsers \
    --key '{"userId": {"S": "u001"}}' \
    --update-expression "SET active = :val" \
    --expression-attribute-values '{":val": {"BOOL": false}}'

# Delete a single item
aws dynamodb delete-item \
    --table-name AppUsers \
    --key '{"userId": {"S": "u001"}}'
