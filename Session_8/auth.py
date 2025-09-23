```python
# Import necessary libraries
from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from your_database import User  # Replace 'your_database' with your actual database

# Create a Blueprint for authentication
auth = Blueprint('auth', __name__)

# Initialize JWTManager
jwt = JWTManager()

# Define a function to create a new user
@auth.route('/register', methods=['POST'])
def register():
    """
    Create a new user.

    Request Body:
    - email (str): Email address of the user
    - password (str): Password of the user

    Returns:
    - A JSON response with the user's ID
    """
    email = request.json.get('email')
    password = request.json.get('password')

    # Check if the email already exists
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'msg': 'Email already exists'}), 400

    # Create a new user
    new_user = User(email=email, password=generate_password_hash(password))
    new_user.save()

    # Return the user's ID
    return jsonify({'msg': 'User created successfully', 'user_id': new_user.id}), 201

# Define a function to login a user
@auth.route('/login', methods=['POST'])
def login():
    """
    Login a user.

    Request Body:
    - email (str): Email address of the user
    - password (str): Password of the user

    Returns:
    - A JSON response with the user's access token
    """
    email = request.json.get('email')
    password = request.json.get('password')

    # Check if the user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'msg': 'Email does not exist'}), 401

    # Check if the password is correct
    if not check_password_hash(user.password, password):
        return jsonify({'msg': 'Incorrect password'}), 401

    # Create an access token
    access_token = create_access_token(identity=user.id)

    # Return the access token
    return jsonify({'access_token': access_token}), 200

# Define a function to protected route
@auth.route('/protected', methods=['GET'])
@jwt_required
def protected():
    """
    A protected route that requires authentication.

    Returns:
    - A JSON response with the user's ID
    """
    # Get the user's ID from the access token
    user_id = get_jwt_identity()

    # Return the user's ID
    return jsonify({'msg': 'Hello, {}'.format(user_id)}), 200
```