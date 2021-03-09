import os


class Config:
    """Set Flask config variables."""

    FLASK_ENV = 'development'
    TESTING = True
    SECRET_KEY = os.urandom(32)
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_DATABASE_URI = postgres://foqldzvfnlnajd:332fa4754d8e2ea38de77b9e795bbd93ee5a641b245c0cbbacddf0aaac127562@ec2-52-44-31-100.compute-1.amazonaws.com:5432/d24h16792mcg0a
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_FOLDER = 'flask_app/static'
    TEMPLATES_FOLDER = 'flask_app/templates'
