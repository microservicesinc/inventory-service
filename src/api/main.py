from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# In-memory database
inventory = [
    {"itemId": "item1", "quantity": 10},
    {"itemId": "item2", "quantity": 5}
]

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    ---
    responses:
      200:
        description: Service is healthy
    """
    return jsonify({"status": "healthy"}), 200

@app.route('/inventory', methods=['GET'])
def list_inventory():
    """
    List all inventory items
    ---
    responses:
      200:
        description: List of inventory items
    """
    return jsonify({"items": inventory}), 200

@app.route('/inventory/<item_id>', methods=['GET'])
def get_inventory(item_id):
    """
    Get inventory item details
    ---
    parameters:
      - name: item_id
        in: path
        type: string
        required: true
        description: The ID of the inventory item
    responses:
      200:
        description: Inventory item details
      404:
        description: Item not found
    """
    item = next((i for i in inventory if i["itemId"] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/inventory/<item_id>', methods=['PUT'])
def update_inventory_stock(item_id):
    """
    Update inventory item stock
    ---
    parameters:
      - name: item_id
        in: path
        type: string
        required: true
        description: The ID of the inventory item
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            quantity:
              type: integer
    responses:
      200:
        description: Inventory updated
      404:
        description: Item not found
    """
    data = request.get_json()
    quantity = data.get("quantity")

    item = next((i for i in inventory if i["itemId"] == item_id), None)
    if item:
        item["quantity"] = quantity
        return jsonify({"status": "success", "item": item}), 200
    
    return jsonify({"error": "Item not found"}), 404

@app.route('/inventory', methods=['POST'])
def update_inventory():
    """
    Update inventory item
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            itemId:
              type: string
            quantity:
              type: integer
    responses:
      201:
        description: Inventory updated
    """
    data = request.get_json()
    item_id = data.get("itemId")
    quantity = data.get("quantity")

    # Check if item exists
    item = next((i for i in inventory if i["itemId"] == item_id), None)
    if item:
        item["quantity"] = quantity
    else:
        inventory.append({"itemId": item_id, "quantity": quantity})

    return jsonify({"status": "success", "item": {"itemId": item_id, "quantity": quantity}}), 201

if __name__ == '__main__':
    app.run(debug=True)
