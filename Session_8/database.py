```python
# database.py

# Import necessary libraries
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Define the database connection URL
DB_URL = os.environ.get('DATABASE_URL')

# Create a database engine
engine = create_engine(DB_URL)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()

# Define a class for the User table
class User(Base):
    """User table definition"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Define a relationship with the Post table
    posts = relationship('Post', backref='author')

# Define a class for the Post table
class Post(Base):
    """Post table definition"""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Define a foreign key relationship with the User table
    author_id = Column(Integer, ForeignKey('users.id'))

# Create all tables in the engine
Base.metadata.create_all(engine)

# Create a session to interact with the database
session = Session()
```