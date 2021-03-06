import os


class Config:
    """Set Flask config variables."""

    FLASK_ENV = 'development'
    TESTING = False
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = 'flask_app/static'
    TEMPLATES_FOLDER = 'flask_app/templates'
