```python
# config.py

"""
Configuration settings for the application
"""

import os
from dotenv import load_dotenv

# Load environment variables from.env file
load_dotenv()

# Define database connection settings
class DatabaseConfig:
    """Database connection settings"""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Define application settings
class AppConfig:
    """Application settings"""
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', default=False)
    TESTING = os.getenv('TESTING', default=False)

# Define email settings
class EmailConfig:
    """Email settings"""
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', default=587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', default=True)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

# Define logging settings
class LoggingConfig:
    """Logging settings"""
    LOG_LEVEL = os.getenv('LOG_LEVEL', default='INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Define production settings
class ProductionConfig:
    """Production settings"""
    DEBUG = False
    TESTING = False

# Define testing settings
class TestingConfig:
    """Testing settings"""
    DEBUG = True
    TESTING = True

# Define development settings
class DevelopmentConfig:
    """Development settings"""
    DEBUG = True
    TESTING = False

# Create a dictionary of configuration settings
config = {
    'database': DatabaseConfig,
    'app': AppConfig,
    'email': EmailConfig,
    'logging': LoggingConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'development': DevelopmentConfig
}

# Set the default configuration
default_config = DevelopmentConfig
```