import pandas as pd
import numpy as np
import pickle
import time
from datetime import date

# Classification ML libraries
from sklearn.model_selection import train_test_split

# Classification model scoring library
from sklearn.metrics import accuracy_score


def evaluate_predictions(y_actual, y_predicted):

    accuracy = accuracy_score(y_actual, y_predicted) * 100
    print(f'Accuracy: {accuracy:.2f}%')

    return accuracy


def calculate_age(birthdate):
    today = date.today().toordinal()
    user_age_in_days = today - birthdate.toordinal()

    return user_age_in_days


cvd_data = pd.read_csv('heart_disease_data/sanitized_cvd_data.csv')

# Randomizes samples for training
cvd_data_shuffled = cvd_data.sample(frac=1)

# Drop the weather description since that is the variable to be predicted
x = cvd_data_shuffled.drop('cardio', axis=1)

# Retrieve only the weather description to test against the model's predictions.
y = cvd_data_shuffled['cardio']

# Split x and y DataFrames into testing and training sets.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# Load the trained model
loaded_model = pickle.load(open('saved_model/cvd_random_forest_classifier_model.pkl', 'rb'))  # ACCURACY == 73.09%
print('Previously saved model loaded.')

# Columns: Age, Height, Weight, Gender, Systolic BP, Diastolic BP,
#           Cholesterol, Glucose, Smoking, Alcohol Intake, Physical Activity
user_selected_age = calculate_age(date(1985, 5, 27))  # patient age IN DAYS
user_selected_height = 66  # patient height
user_selected_weight = 185  # patient weight
user_selected_gender = 1  # 1 = male, 0 = female
user_selected_sbp = 118  # systolic bp
user_selected_dbp = 78  # diastolic bp
user_selected_cholesterol = 222  # cholesterol measurement
user_selected_glucose = 103  # blood glucose measurement
user_selected_smoking = 0  # smokes: 1 = yes, 0 = no
user_selected_alcohol = 1  # consumes alcohol: 1 = yes, 0 = no
user_selected_active = 1  # physically active: 1 = yes, 0 = no

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

# Uses loaded model to make a prediction with user input
indicator = loaded_model.predict(user_selections[:])

# Scores the model's prediction accuracy
score = loaded_model.score(x_test, y_test) * 100

if indicator == 0:
    print(f'There is a {score:.2f}% chance you do not have heart disease.')
elif indicator == 1:
    print(f'Unfortunately there is a {score:.2f}% you could have heart disease.')

