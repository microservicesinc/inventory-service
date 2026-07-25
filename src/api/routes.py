from flask import Flask, jsonify, request
from flasgger import Swagger
from src.database import (
    update_stock_atomic, 
    get_stock_balance, 
    scan_all_inventory
)

app = Flask(__name__)
swagger = Swagger(app)

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
    try:
        items = scan_all_inventory()
        return jsonify({"items": items}), 200
    except Exception as e:
        return jsonify({"error": f"Internal database error: {str(e)}"}), 500

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
    try:
        db_item = get_stock_balance(item_id)
        
        # Verify item metadata signature exists in the database
        if "stock" in db_item and "SK" in db_item:
            return jsonify({
                "itemId": item_id,
                "quantity": int(db_item["stock"])
            }), 200
            
        return jsonify({"error": "Item not found"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve record: {str(e)}"}), 500

@app.route('/inventory/<item_id>', methods=['PUT'])
def update_inventory_stock_endpoint(item_id):
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
    try:
        data = request.get_json() or {}
        if "quantity" not in data:
            return jsonify({"error": "Missing quantity property"}), 400
            
        quantity = int(data["quantity"])

        # Look up current item state to calculate the atomic mathematical difference
        db_item = get_stock_balance(item_id)
        if "SK" not in db_item:
            return jsonify({"error": "Item not found"}), 404

        current_stock = int(db_item.get("stock", 0))
        adjustment = quantity - current_stock
        
        # Apply the step mutation securely via Atomic Counter expressions
        updated_attrs = update_stock_atomic(item_id, adjustment)
        
        return jsonify({
            "status": "success", 
            "item": {"itemId": item_id, "quantity": int(updated_attrs.get("stock", 0))}
        }), 200
    except Exception as e:
        return jsonify({"error": f"Stock adjustment transaction failed: {str(e)}"}), 500

@app.route('/inventory', methods=['POST'])
def create_or_overwrite_inventory():
    """
    Create or update inventory item
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
    try:
        data = request.get_json() or {}
        item_id = data.get("itemId")
        quantity = data.get("quantity")

        if not item_id or quantity is None:
            return jsonify({"error": "Missing itemId or quantity parameters"}), 400

        quantity = int(quantity)

        # Check existing table items to compute baseline differential
        db_item = get_stock_balance(item_id)
        current_stock = int(db_item.get("stock", 0)) if "SK" in db_item else 0
        adjustment = quantity - current_stock
        
        # Commit the item initialization or mutation atomically
        updated_attrs = update_stock_atomic(item_id, adjustment)

        return jsonify({
            "status": "success", 
            "item": {"itemId": item_id, "quantity": int(updated_attrs.get("stock", 0))}
        }), 201
    except Exception as e:
        return jsonify({"error": f"Record compilation failure: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
