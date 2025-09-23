```python
# Import necessary dependencies
import os
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS for cross-origin resource sharing
CORS(app)

# Configure the Flask application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

# Initialize the database and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Initialize the Bcrypt and JWTManager
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Define the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Define the schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

# Initialize the schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Define the routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(username=data['username'], password=bcrypt.generate_password_hash(data['password']).decode('utf-8'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify(user_schema.dump(new_user))

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products))

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(product_schema.dump(new_product))

# Define the error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Internal server error'}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
```

This code defines a Flask application with the following features:

*   It uses Flask-SQLAlchemy for database operations and Flask-Marshmallow for schema validation.
*   It enables CORS for cross-origin resource sharing.
*   It uses Flask-Bcrypt for password hashing and Flask-JWT-Extended for JSON Web Token (JWT) management.
*   It defines two models: `User` and `Product`, with corresponding schemas for validation.
*   It defines several routes for creating and retrieving users and products.
*   It includes error handlers for 404 and 500 errors.
*   It runs the application in debug mode when executed directly.