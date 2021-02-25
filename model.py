import pandas as pd
import numpy as np
import pickle

# Classification ML libraries
from sklearn.model_selection import train_test_split

# Classification model scoring library
from sklearn.metrics import accuracy_score

# Array to store dict of string(s) to describe test results
result_string = []


def evaluate_predictions(y_actual, y_predicted):
    """
    Runs model to compare predictions to actual results for a numerical representation of the model's accuracy
    at the moment the model is used.
    :param y_actual:
    :param y_predicted:
    :return:
    """

    accuracy = accuracy_score(y_actual, y_predicted) * 100  # Scores accuracy of model's prediction
    print(f'Accuracy: {accuracy:.2f}%')

    return accuracy


def read_data_file():
    """
    Uses pandas to read in stored data file to assess accuracy.
    :return:
    """
    cvd_data = pd.read_csv('flask_app/static/data/sanitized_cvd_data.csv')

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
    # Columns: Age, Height, Weight, Gender, Systolic BP, Diastolic BP,
    #           Cholesterol, Glucose, Smoking, Alcohol Intake, Physical Activity

    user_selected_age = user_form_submissions[0]['age']
    user_selected_height = user_form_submissions[1]['height']  # patient height
    user_selected_weight = user_form_submissions[2]['weight']  # patient weight
    user_selected_gender = user_form_submissions[3]['gender']  # 2 = male, 1 = female
    user_selected_sbp = user_form_submissions[4]['systolic_bp']  # systolic bp
    user_selected_dbp = user_form_submissions[5]['diastolic_bp']  # diastolic bp
    # blood glucose measurement 1= normal, 2= above, 3= well above
    user_selected_glucose = user_form_submissions[6]['blood_glucose']
    # cholesterol measurement 1= normal, 2= above, 3= well above
    user_selected_cholesterol = user_form_submissions[7]['cholesterol']
    user_selected_smoking = user_form_submissions[8]['alcohol_intake']  # smokes: 1 = yes, 0 = no
    user_selected_alcohol = user_form_submissions[9]['current_smoker']  # consumes alcohol: 1 = yes, 0 = no
    user_selected_active = user_form_submissions[10]['physically_active']  # physically active: 1 = yes, 0 = no

    # Convert user input to Numpy array and use for data to predict with model
    # Reshaped and used as a record with a single row
    user_selections = np.array([user_selected_age,
                                user_selected_height,
                                user_selected_weight,
                                user_selected_gender,
                                user_selected_sbp,
                                user_selected_dbp,
                                user_selected_cholesterol,
                                user_selected_glucose,
                                user_selected_smoking,
                                user_selected_alcohol,
                                user_selected_active]).reshape(1, -1)

    return user_selections


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

    # Scores the model's prediction accuracy
    x_train, x_test, y_train, y_test = determine_test_sets(read_data_file())
    score = loaded_model.score(x_test, y_test) * 100

    if cvd_prediction == 0:
        result_string.append({'result': f'There is a {score:.2f}% chance you do not have heart disease.'})
    elif cvd_prediction == 1:
        result_string.append({'result': f'Unfortunately there is a {score:.2f}% you could have heart disease.'})

    return score, result_string


def initiate_model(user_data):
    """
    Runs and scores the model using the user's input.
    :param user_data:
    :return:
    """

    user_input = parse_user_input(user_data)
    loaded_model = load_trained_model()

    cvd_prediction_result = run_model(loaded_model, user_input)

    prediction_accuracy_score, prediction_result_string = score_model(cvd_prediction_result, loaded_model)

    return cvd_prediction_result, prediction_accuracy_score, prediction_result_string





