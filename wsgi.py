"""Application entry point."""
from flask_app import init_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

app = init_app()

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30), unique=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    app.run()
