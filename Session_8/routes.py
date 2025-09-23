```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Define schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class BlogPostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlogPost

# Define routes
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(username=data['username'], email=data['email'], password=generate_password_hash(data['password']))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/posts', methods=['GET'])
@jwt_required
def get_posts():
    posts = BlogPost.query.all()
    return jsonify([post.to_dict() for post in posts])

@app.route('/posts', methods=['POST'])
@jwt_required
def create_post():
    data = request.json
    post = BlogPost(title=data['title'], content=data['content'], user_id=get_jwt_identity())
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201

@app.route('/posts/<int:post_id>', methods=['GET'])
@jwt_required
def get_post(post_id):
    post = BlogPost.query.get(post_id)
    if post:
        return jsonify(post.to_dict())
    return jsonify({'message': 'Post not found'}), 404

@app.route('/posts/<int:post_id>', methods=['PUT'])
@jwt_required
def update_post(post_id):
    post = BlogPost.query.get(post_id)
    if post:
        data = request.json
        post.title = data['title']
        post.content = data['content']
        db.session.commit()
        return jsonify(post.to_dict())
    return jsonify({'message': 'Post not found'}), 404

@app.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required
def delete_post(post_id):
    post = BlogPost.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({'message': 'Post deleted successfully'})
    return jsonify({'message': 'Post not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
```