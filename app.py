# app.py (At the root of your project)
import os
import sys

# Ensure Python can discover modules inside the src/ folder correctly
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.api.routes import app

if __name__ == '__main__':
    # Bootstraps Flask locally on Port 5000 with auto-reload enabled
    print("🚀 Starting Inventory Microservice API...")
    print("📖 Swagger UI available at: http://localhost:5000/apidocs/")
    app.run(host="0.0.0.0", port=5000, debug=True)
