```markdown
# Task Management Web Application

## Table of Contents

1. [Setup](#setup)
2. [Dependencies](#dependencies)
3. [Database Setup](#database-setup)
4. [User Authentication](#user-authentication)
5. [Task Management](#task-management)
6. [Error Handling](#error-handling)
7. [Deployment](#deployment)

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create a new database
python database.py

# Create a new user
python user.py
```

## Dependencies

```python
import os
import sqlite3
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
```

## Database Setup

```python
# database.py
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                due_date DATE NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()
```

## User Authentication

```python
# user.py
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class UserManager:
    def __init__(self):
        self.users = {}

    def create_user(self, username, password):
        self.users[username] = User(len(self.users), username, password)

    def get_user(self, username):
        return self.users.get(username)

    def login(self, username, password):
        user = self.get_user(username)
        if user and user.check_password(password):
            login_user(user)
            return True
        return False

    def logout(self):
        logout_user()
```

## Task Management

```python
# task.py
class Task:
    def __init__(self, id, title, description, due_date):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = False

class TaskManager:
    def __init__(self):
        self.tasks = {}

    def create_task(self, title, description, due_date):
        self.tasks[len(self.tasks)] = Task(len(self.tasks), title, description, due_date)

    def get_task(self, id):
        return self.tasks.get(id)

    def update_task(self, id, title, description, due_date):
        task = self.get_task(id)
        if task:
            task.title = title
            task.description = description
            task.due_date = due_date

    def delete_task(self, id):
        del self.tasks[id]
```

## Error Handling

```python
# error.py
class Error(Exception):
    pass

class DatabaseError(Error):
    def __init__(self, message):
        self.message = message

class UserError(Error):
    def __init__(self, message):
        self.message = message

class TaskError(Error):
    def __init__(self, message):
        self.message = message
```

## Deployment

```bash
# Run the application
python app.py

# Access the application at http://localhost:5000
```

```python
# app.py
from flask import Flask
from database import Database
from user import UserManager
from task import TaskManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

db = Database()
user_manager = UserManager()
task_manager = TaskManager()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = task_manager.tasks.values()
    return jsonify([{'id': task.id, 'title': task.title, 'description': task.description, 'due_date': task.due_date} for task in tasks])

@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']
    due_date = request.json['due_date']
    task_manager.create_task(title, description, due_date)
    return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'due_date': task.due_date})

@app.route('/users', methods=['GET'])
def get_users():
    users = user_manager.users.values()
    return jsonify([{'id': user.id, 'username': user.username} for user in users])

@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    user_manager.create_user(username, password)
    return jsonify({'id': user.id, 'username': user.username})

if __name__ == '__main__':
    app.run(debug=True)
```