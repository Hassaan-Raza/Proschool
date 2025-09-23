```python
# Import necessary libraries
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize Flask app and extensions
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a random secret key
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Define User schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

# Define User service
class UserService:
    def __init__(self):
        self.users = []

    def create_user(self, username, password):
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return user

    def get_user(self, username):
        return User.query.filter_by(username=username).first()

    def authenticate(self, username, password):
        user = self.get_user(username)
        if user and check_password_hash(user.password, password):
            return user
        return None

# Initialize User service
user_service = UserService()

# Define authentication routes
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = user_service.authenticate(username, password)
    if user:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    user = user_service.create_user(username, password)
    return jsonify({'message': 'User created successfully'}), 201

# Define protected route
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user}'}), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
```