```python
# Import necessary libraries
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt

# Create a new Flask application
app = Flask(__name__)

# Enable CORS for cross-origin resource sharing
CORS(app)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Initialize the Bcrypt for password hashing
bcrypt = Bcrypt(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Define the User schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

# Define the Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Define the Product schema
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

# Create the database tables
with app.app_context():
    db.create_all()

# Define a route for creating a new user
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    user = User(username=data['username'], password=bcrypt.generate_password_hash(data['password']).decode('utf-8'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Define a route for getting all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users])

# Define a route for getting a user by ID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'username': user.username})
    return jsonify({'message': 'User not found'}), 404

# Define a route for creating a new product
@app.route('/product', methods=['POST'])
def create_product():
    data = request.json
    product = Product(name=data['name'], price=data['price'])
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

# Define a route for getting all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': product.id, 'name': product.name, 'price': product.price} for product in products])

# Define a route for getting a product by ID
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({'id': product.id, 'name': product.name, 'price': product.price})
    return jsonify({'message': 'Product not found'}), 404

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```