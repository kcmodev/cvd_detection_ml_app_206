"""Routes for parent Flask app."""
from flask import render_template, request, json, session, redirect
from flask import current_app as app
from flask_app import model
from flask_login import login_user, login_required, logout_user


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    """
    Route for landing page
    :return:
    """

    return render_template('index.html', title='Login')


@app.route('/login', methods=['POST'])
def user_login():
    """
    Route for posting user credential verification. POST only.
    :return:
    """

    from wsgi import User  # import User class to query databse

    # Retrieve user input from login form
    entered_username = request.form['user']
    entered_passwd = request.form['password']

    # Query database
    user = User.query.filter_by(
        username=entered_username, password=entered_passwd).first()

    if user:  # True if user exists in database
        login_user(user)

    return redirect('/determine_risk')


@app.route('/determine_risk', methods=['GET'])
@login_required
def user_variables_page():
    """
    Renders form to accept user input for model prediction
    :return:
    """

    return render_template('determine_risk.html', title='Determine Risk')


@app.route('/calculated_risk_results', methods=['POST'])
@login_required
def show_risk_results():
    """
    Take POST request and saves user input as session JSON object.
    :return:
    """

    # get JSON from ajax request to pass user input to model
    session['json'] = request.get_json()
    return json.dumps({'success': True}), 200


@app.route('/calculated_risk_results', methods=['GET'])
@login_required
def show_risk_results_page():
    """
    Takes GET request, uses session data to determine and display results.
    :return:
    """

    user_input = session['json']  # loads user from session data

    # runs model to make the prediction
    cvd_result, model_score, result_string, high_risk_categories = model.initiate_model(
        user_input)
    return render_template('calculated_risk_results.html',
                           title='Results',
                           user_data=user_input,
                           cvd_result=cvd_result,
                           model_score_string=model_score,
                           result_string=result_string,
                           categories=high_risk_categories)


@app.route('/dashapp', methods=['GET'])
@login_required
def dashboard_page():
    """
    Redirects to Plotly dashboard for all data visualizations.
    :return:
    """

    return redirect('/dashapp/')


@app.route('/logout', methods=['GET'])
def logout_user_and_clear_session_data():
    """
    Clears session data, logs out user, and redirects to the login screen.
    :return:
    """

    session.clear()
    logout_user()
    return redirect('/index')
