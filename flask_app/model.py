import pandas as pd
import numpy as np
import pickle

# Classification ML libraries
from sklearn.model_selection import train_test_split


def read_data_file():
    """
    Uses pandas to read in stored data file to assess accuracy.
    :return:
    """
    cvd_data = pd.read_csv('flask_app/static/data/sanitized_raw_cvd_data.csv')

    return cvd_data


def determine_test_sets(data):
    """
    Determines size of training and testing data sets.
    :param data:
    :return:
    """

    # Randomizes samples for training
    cvd_data_shuffled = data.sample(frac=1)

    # Drop the weather description since that is the variable to be predicted
    x = cvd_data_shuffled.drop('cardio', axis=1)

    # Retrieve only the weather description to test against the model's predictions.
    y = cvd_data_shuffled['cardio']

    # Split x and y DataFrames into testing and training sets.
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    return x_train, x_test, y_train, y_test


def load_trained_model():
    """
    Loads saved pickle file of the trained model.
    :return:
    """
    # Load the trained model
    file = open('flask_app/static/saved_model/cvd_random_forest_classifier_model.pkl', 'rb')
    loaded_model = pickle.load(file)

    return loaded_model


def parse_user_input(user_form_submissions):
    """
    Collects form data to use as user input for the model to use to make a prediction.
    :param user_form_submissions:
    :return:
    """
    high_risk_categories = {}

    # Columns: Age, Height, Weight, Gender, Systolic BP, Diastolic BP,
    #           Cholesterol, Glucose, Smoking, Alcohol Intake, Physical Activity
    user_selected_age = user_form_submissions[0]['age']
    user_selected_height = int(user_form_submissions[1]['height'])  # patient height
    user_selected_weight = int(user_form_submissions[2]['weight'])  # patient weight
    user_selected_gender = user_form_submissions[3]['gender']  # 2 = male, 1 = female
    user_selected_sbp = int(user_form_submissions[4]['systolic_bp'])  # systolic bp

    if user_selected_sbp > 130:
        high_risk_categories['Blood Pressure'] = 'Systolic Blood Pressure over 130mm/Hg'

    user_selected_dbp = user_form_submissions[5]['diastolic_bp']  # diastolic bp

    user_bmi = int(user_selected_weight // ((user_selected_height / 100) ** 2))

    if user_bmi > 25:
        high_risk_categories['BMI'] = f'Body Mass Index of {user_bmi}'

    # blood glucose measurement 1= normal, 2= above, 3= well above
    user_selected_glucose = user_form_submissions[6]['blood_glucose']

    # cholesterol measurement 1= normal, 2= above, 3= well above
    user_selected_cholesterol = int(user_form_submissions[7]['cholesterol'])

    if user_selected_cholesterol == 3:
        high_risk_categories['Cholesterol'] = 'Cholesterol well above normal.'

    user_selected_alcohol = user_form_submissions[8]['alcohol_intake']  # smokes: 1 = yes, 0 = no
    user_selected_smoking = user_form_submissions[9]['current_smoker']  # consumes alcohol: 1 = yes, 0 = no
    user_selected_active = user_form_submissions[10]['physically_active']  # physically active: 1 = yes, 0 = no

    # Convert user input to Numpy array and use for data to predict with model
    # Reshaped and used as a record with a single row
    user_selections = np.array([user_selected_age,
                                user_selected_height,
                                user_selected_weight,
                                user_bmi,
                                user_selected_gender,
                                user_selected_sbp,
                                user_selected_dbp,
                                user_selected_cholesterol,
                                user_selected_glucose,
                                user_selected_smoking,
                                user_selected_alcohol,
                                user_selected_active]).reshape(1, -1)

    if len(user_form_submissions) == 12:
        high_risk_categories['pretty_old'] = f'You also happen to be the oldest person in history ' \
                                             f'at {user_form_submissions[11]["pretty_old"]} years old! ' \
                                             f'Some call it a risk factor, I call it a badge of honor ;). ' \
                                             f'Should probably still go get a checkup though.'

    return user_selections, high_risk_categories


def run_model(loaded_model, user_selections):
    # Uses loaded model to make a prediction with user input
    cvd_prediction = loaded_model.predict(user_selections[:])

    return cvd_prediction


def score_model(cvd_prediction, loaded_model):
    """
    Uses the model's prediction and the score to generate a result for the user and a percent likelihood
    it is correct.
    :param cvd_prediction:
    :param loaded_model:
    :return:
    """

    result_string = ""

    # Scores the model's prediction accuracy
    x_train, x_test, y_train, y_test = determine_test_sets(read_data_file())
    score = loaded_model.score(x_test, y_test) * 100

    if cvd_prediction == 0:
        result_string = f'You have a low risk of either having or developing heart disease.'
    elif cvd_prediction == 1:
        result_string = f'You are at a high risk of developing heart disease. Please consult with a physician.'

    accuracy_string = f"Model accuracy score: {score:.2f}%."

    return accuracy_string, result_string


def initiate_model(user_data):
    """
    Runs and scores the model using the user's input.
    :param user_data:
    :return:
    """

    user_input, user_high_risk_categories = parse_user_input(user_data)
    loaded_model = load_trained_model()

    cvd_prediction_result = run_model(loaded_model, user_input)

    prediction_accuracy_score, prediction_result_string = score_model(cvd_prediction_result, loaded_model)

    return cvd_prediction_result, prediction_accuracy_score, prediction_result_string, user_high_risk_categories





