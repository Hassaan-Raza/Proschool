```python
# models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """Custom user model manager that uses email instead of username"""
    
    def create_user(self, email, password=None):
        """Create and return a `User` with an email and password."""
        
        if not email:
            raise ValueError(_('Users must have an email address'))
        
        email = self.normalize_email(email)
        user = self.model(email=email)
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password):
        """Create and return a `User` with superuser (admin) permissions."""
        
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that uses email instead of username"""
    
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email

class BlogPost(models.Model):
    """Blog post model"""
    
    title = models.CharField(_('title'), max_length=255)
    content = models.TextField(_('content'))
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    def __str__(self):
        return self.title
```