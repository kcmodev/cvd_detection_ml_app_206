import os

class Config:
    """Set Flask config variables."""

    FLASK_ENV = 'development'
    TESTING = True
    # SECRET_KEY = environ.get('SECRET_KEY')
    # SECRET_KEY = os.urandom(32)
    STATIC_FOLDER = 'flask_app/static'
    TEMPLATES_FOLDER = 'flask_app/templates'
