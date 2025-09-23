```python
"""
Main entry point for the application.
"""

# Import necessary libraries
import os
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS for cross-origin resource sharing
CORS(app)

# Configure the application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a secure secret key

# Initialize the database and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Initialize the JWT manager
jwt = JWTManager(app)

# Import models and routes
from models import User, Item
from routes import user_routes, item_routes

# Register routes
app.register_blueprint(user_routes)
app.register_blueprint(item_routes)

# Create the database tables
with app.app_context():
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
```