"""App entry point."""
from flask_app import init_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

# initializes a flask app and then a plotly dashboard with the flask app as the server
app = init_app()

# inits a SQLAlchemy database to store use credentials
db = SQLAlchemy(app)

# Manages user session login status
login_manager = LoginManager()
login_manager.init_app(app)


# User class for instantiating user objects
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30), unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password


# Allows searching the database for the user by id and subsequently loading the user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    app.run()
