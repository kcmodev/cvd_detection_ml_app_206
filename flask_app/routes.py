"""Routes for parent Flask app."""
from flask import render_template, request, json, session, redirect, make_response
from flask import current_app as app
import model


@app.route('/')
@app.route('/index')
def index():
    """
    Renders login screen
    :return:
    """
    return render_template('index.html', title='Login')


@app.route('/determine_risk')
def user_variables_page():
    """
    Renders form to accept user input
    :return:
    """
    # if request.method == 'POST':
    # session.clear()
    # return json.dumps({'success': True}), 200

    return render_template('determine_risk.html', title='Vitals')


@app.route('/calculated_risk_results', methods=['POST'])
def show_risk_results():
    """
    Take POST request and saves user input as session data.
    :return:
    """

    if request.method == 'POST':
        session['json'] = request.get_json()  # get JSON from ajax request to pass user input to model

        return json.dumps({'success': True}), 200


@app.route('/calculated_risk_results')
def show_risk_results_page():
    """
    Takes GET request, uses session data to determine and display results.
    :return:
    """
    user_input = session['json']  # saves user form submission as session data
    cvd_result, model_score, result_string = model.initiate_model(user_input)  # runs model to make the prediction
    return render_template('calculated_risk_results.html',
                           title='Results',
                           user_data=user_input,
                           cvd_result=cvd_result,
                           model_score=model_score,
                           result_string=result_string)


@app.route('/dashapp')
def dashboard_page():
    """
    Redirects to Plotly dashboard.
    :return:
    """

    return redirect('/dashapp/')


@app.route('/logout')
def logoff():
    """
    Clears session data and returns user to the login screen.
    :return:
    """
    session.clear()
    return json.dumps({'success': True}), 200
