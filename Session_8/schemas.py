```python
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    """Base model for user data"""
    username: str
    email: str
    is_active: bool

class UserCreate(UserBase):
    """Model for user creation"""
    password: str

class User(UserBase):
    """Model for user data"""
    id: int
    password: str

class UserUpdate(BaseModel):
    """Model for user update"""
    username: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]

class UserResponse(BaseModel):
    """Model for user response"""
    id: int
    username: str
    email: str
    is_active: bool

class Token(BaseModel):
    """Model for token data"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Model for token data"""
    username: str
    is_active: bool
```