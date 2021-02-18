"""Routes for parent Flask app."""
from flask import render_template, request, json, session
from flask import current_app as app

from model import initiate_model


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Login')


@app.route('/determine_risk')
def user_variables_page():
    return render_template('determine_risk.html', title='Vitals')


@app.route('/calculated_risk_results', methods=['POST', 'GET'])
def show_risk_results():

    if request.method == 'POST':
        print(f'post form data: {request.get_json()}')
        session['json'] = request.get_json()
        return json.dumps({'success': True}), 200

    user_input = session['json']
    print(f'session json: {user_input} type: {type(user_input)}')
    initiate_model(user_input)

    return render_template('calculated_risk_results.html', title='Results', user_data=user_input)

# @app.route('/dashapp/')
# def dashboard_page():
#     return render_template('data.html')
