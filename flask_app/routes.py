"""Routes for parent Flask app."""
from flask import render_template
from flask import current_app as app

from model import run_model

user = {'name': 'Steve'}


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', name=user['name'], title='Login')


@app.route('/determine_risk')
def data_page():
    # return render_template('data.html', name=user['name'], title='Data')
    return render_template('determine_risk.html')


@app.route('/show_calculated_risk')
def calculated_risk_page():

    return render_template('show_calculated_risk.html')


# @app.route('/dashapp/')
# def dashboard_page():
#     return render_template('determine_risk.html')
