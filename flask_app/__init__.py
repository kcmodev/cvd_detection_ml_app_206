"""Initialize Flask app."""
from flask import Flask


def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    with app.app_context():
        # Import routes from core Flask app
        from . import routes

        # Initialize Plotly Dash app dashboard using Flask as the server
        from .plotly.dashboard import init_dashboard
        app = init_dashboard(app)

        return app
