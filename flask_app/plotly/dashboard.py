import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
        ]
    )
    # assume you have a "long-form" data frame
    # see https://plotly.com/python/px-arguments/ for more options
    # df = pd.DataFrame({
    #     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    #     "Amount": [4, 1, 2, 2, 4, 5],
    #     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    # })

    # Columns: Age, Height, Weight, Gender, Systolic BP, Diastolic BP,
    #           Cholesterol, Glucose, Smoking, Alcohol Intake, Physical Activity

    # columns = [{'age': 'Column 1'},
    #            {'gender': 'Column 2'},
    #            {'height': 'column 3'},
    #            {'weight': 'column 4'},
    #            {'ap_hi': 'column 5'},
    #            {'ap_lo': 'column 6'},
    #            {'cholesterol': 'column 7'},
    #            {'gluc': 'column 8'},
    #            {'smoke': 'column 9'},
    #            {'alco': 'column 10'},
    #            {'active': 'column 11'},
    #            {'cardio': 'column 12'}]

    columns = ['age', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo',
               'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'cardio']

    df = pd.read_csv("flask_app/static/data/sanitized_cvd_data.csv")
    cholest = df['cholesterol']
    age = df['age']

    # fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
    # fig2 = px.scatter(df, x='Fruit', y='Amount')

    fig = px.density_heatmap(df, x=age, y=cholest)

    # Create Dash Layout
    # dash_app.layout = html.Div(id='dash-container')
    dash_app.layout = html.Div(children=[
        html.H1(children='Hello Dasher'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )

        # html.Div(children='''
        #     Dash: Another web application framework for Python.
        # '''),
        #
        # dcc.Graph(
        #     id='example-graph-2',
        #     figure=fig2
        # )
    ])

    return dash_app.server
