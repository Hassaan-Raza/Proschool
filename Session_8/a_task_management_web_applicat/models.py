```python
# Import necessary dependencies
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from datetime import datetime

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

# Define the User model
class User(db.Model, UserMixin):
    """
    User model representing a user in the application.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)

    def set_password(self, password):
        """
        Set the password for the user.
        
        :param password: The password to be set.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the provided password matches the stored password hash.
        
        :param password: The password to be checked.
        :return: True if the password is correct, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

# Define the Task model
class Task(db.Model):
    """
    Task model representing a task in the application.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Task('{self.title}', '{self.description}', '{self.due_date}')"
```