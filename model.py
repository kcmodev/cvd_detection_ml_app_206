import pandas as pd
import numpy as np
import pickle
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# Classification ML libraries
from sklearn.model_selection import train_test_split

# Classification model scoring library
from sklearn.metrics import accuracy_score


def evaluate_predictions(y_actual, y_predicted):

    accuracy = accuracy_score(y_actual, y_predicted) * 100  # Scores accuracy of model's prediction
    print(f'Accuracy: {accuracy:.2f}%')

    return accuracy


def convert_birthdate_to_age_in_days(birthdate):
    today = date.today().toordinal()  # Converts today's date into the total number of days since epoch
    user_age_in_days = today - birthdate.toordinal()  # Converts birthday to days since epoch and subtracts from today

    return user_age_in_days


def convert_age_in_days_to_years(birthdate_in_days):
    delta = relativedelta(date.today(), date.fromordinal(birthdate_in_days))
    years = datetime.today().year - (delta.years + 1)

    return years


def read_data_file():
    cvd_data = pd.read_csv('heart_disease_data/sanitized_cvd_data.csv')

    return cvd_data


def determine_test_sets(data):
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
    # Load the trained model
    loaded_model = pickle.load(open('saved_model/cvd_random_forest_classifier_model.pkl', 'rb'))  # ACCURACY == 73.09%
    print('Previously saved model loaded.')


def collect_user_input(user_form_submissions):
    # Columns: Age, Height, Weight, Gender, Systolic BP, Diastolic BP,
    #           Cholesterol, Glucose, Smoking, Alcohol Intake, Physical Activity

    print(f'input function params: {user_form_submissions}')

    user_selected_age = user_form_submissions[0]['age']  # patient age IN DAYS
    user_selected_height = user_form_submissions[1]['height']  # patient height
    user_selected_weight = user_form_submissions[2]['weight']  # patient weight
    user_selected_gender = user_form_submissions[3]['gender']  # 2 = male, 1 = female
    user_selected_sbp = user_form_submissions[4]['systolic_bp']  # systolic bp
    user_selected_dbp = user_form_submissions[5]['diastolic_bp']  # diastolic bp
    user_selected_glucose = user_form_submissions[6]['blood_glucose']  # blood glucose measurement 1= normal, 2= above, 3= well above
    user_selected_cholesterol = user_form_submissions[7]['cholesterol']  # cholesterol measurement 1= normal, 2= above, 3= well above
    user_selected_smoking = user_form_submissions[8]['alcohol_intake']  # smokes: 1 = yes, 0 = no
    user_selected_alcohol = user_form_submissions[9]['current_smoker']  # consumes alcohol: 1 = yes, 0 = no
    user_selected_active = user_form_submissions[10]['physically_active']  # physically active: 1 = yes, 0 = no



    # user_selected_age = convert_age_in_days_to_years(date(1985, 5, 27))  # patient age IN DAYS
    # user_selected_height = 66  # patient height
    # user_selected_weight = 185  # patient weight
    # user_selected_gender = 1  # 1 = male, 0 = female
    # user_selected_sbp = 118  # systolic bp
    # user_selected_dbp = 78  # diastolic bp
    # user_selected_cholesterol = 1  # cholesterol measurement 1= normal, 2= above, 3= well above
    # user_selected_glucose = 1  # blood glucose measurement 1= normal, 2= above, 3= well above
    # user_selected_smoking = 0  # smokes: 1 = yes, 0 = no
    # user_selected_alcohol = 1  # consumes alcohol: 1 = yes, 0 = no
    # user_selected_active = 1  # physically active: 1 = yes, 0 = no

    # Convert user input to Numpy array and use for data to predict with model
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
    indicator = loaded_model.predict(user_selections[:])


# def score_model(x_test, y_test):
#     # Scores the model's prediction accuracy
#     score = loaded_model.score(x_test, y_test) * 100
#
#     if indicator == 0:
#         print(f'There is a {score:.2f}% chance you do not have heart disease.')
#     elif indicator == 1:
#         print(f'Unfortunately there is a {score:.2f}% you could have heart disease.')


def initiate_model(user_data):
    collect_user_input(user_data)

