"""Routes for parent Flask app."""
from flask import render_template
from flask import current_app as app

# from flask import Flask, render_template, request

# app = Flask(__name__, template_folder='flask_app/templates', static_folder='flask_app/static')
# app = Flask(__name__)
# app.config.from_object('config.Config')

user = {'name': 'Steve'}


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name=user['name'], title='Login')


@app.route('/data')
def data_page():
    # return render_template('data.html', name=user['name'], title='Data')
    return render_template('determine_risk.html')


# @app.route('/dashapp/')
# def dashboard_page():
#     return render_template('determine_risk.html')
