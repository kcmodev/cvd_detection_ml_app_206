"""Routes for parent Flask app."""
from flask import render_template, request, json, session, redirect
from flask import current_app as app
from flask_app import model, log


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    """
    Renders login screen and initiates session token to validate login
    :return:
    """

    session['logged_in'] = False

    return render_template('index.html', title='Login')


@app.route('/login', methods=['POST'])
def user_login():
    username, passwd = log.creds()
    entered_username = request.form['user']
    entered_passwd = request.form['password']

    if entered_username == username and entered_passwd == passwd:
        session['logged_in'] = True
        return redirect('/determine_risk')
    else:
        return redirect('/index')


@app.route('/determine_risk', methods=['GET'])
def user_variables_page():
    """
    Renders form to accept user input
    :return:
    """

    if session['logged_in']:
        return render_template('determine_risk.html', title='Determine Risk')
    else:
        return redirect('/index')


@app.route('/calculated_risk_results', methods=['POST'])
def show_risk_results():
    """
    Take POST request and saves user input as session data.
    :return:
    """

    if session['logged_in']:
        if request.method == 'POST':
            session['json'] = request.get_json()  # get JSON from ajax request to pass user input to model
            return json.dumps({'success': True}), 200
    else:
        return redirect('/index')


@app.route('/calculated_risk_results', methods=['GET'])
def show_risk_results_page():
    """
    Takes GET request, uses session data to determine and display results.
    :return:
    """

    if session['logged_in']:
        user_input = session['json']  # saves user form submission as session data
        cvd_result, model_score, result_string, high_risk_categories = model.initiate_model(user_input)  # runs model to make the prediction
        return render_template('calculated_risk_results.html',
                               title='Results',
                               user_data=user_input,
                               cvd_result=cvd_result,
                               model_score=model_score,
                               result_string=result_string,
                               categories=high_risk_categories)
    else:
        return redirect('/index')


@app.route('/dashapp', methods=['GET'])
def dashboard_page():
    """
    Redirects to Plotly dashboard.
    :return:
    """

    if session['logged_in']:
        return redirect('/dashapp/')
    else:
        return redirect('/index')


@app.route('/logout', methods=['GET'])
def logout_user_and_clear_session_data():
    """
    Clears session data and returns user to the login screen.
    :return:
    """

    session.clear()
    return redirect('/index')
