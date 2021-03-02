import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import plotly.express as px
import pandas as pd


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/css/data.css'
        ]
    )

    # Columns: Age, Height, Weight, Gender, Systolic BP, Diastolic BP,
    #           Cholesterol, Glucose, Smoking, Alcohol Intake, Physical Activity
    df = pd.read_csv("flask_app/static/data/readable_cvd_data.csv")
    cholesterol = df['Cholesterol']
    age = df['Age (years)']
    height = df['Height (cm)']
    weight = df['Weight (kg)']
    gender = df['Gender']
    cvd_status = df['CVD Status']

    # Retrieves smoker data from the imported dataframe and correlates it to whether the patient/user is a smoker
    # smoker_pos_cvd = len(df[(df['Smoker'] == 'yes') & df['CVD Status'].isin(['positive'])])
    # smoker_neg_cvd = len(df[(df['Smoker'] == 'yes') & df['CVD Status'].isin(['negative'])])
    # non_smoker_pos_cvd = len(df[(df['Smoker'] == 'no') & df['CVD Status'].isin(['positive'])])
    # non_smoker_neg_cvd = len(df[(df['Smoker'] == 'no') & df['CVD Status'].isin(['negative'])])

    smoker_pos_cvd = len(df[(df['Cholesterol'] == 'well above normal') & df['CVD Status'].isin(['positive'])])
    smoker_neg_cvd = len(df[(df['Cholesterol'] == 'well above normal') & df['CVD Status'].isin(['negative'])])
    non_smoker_pos_cvd = len(df[(df['Cholesterol'] == 'above normal') & df['CVD Status'].isin(['positive'])])
    non_smoker_neg_cvd = len(df[(df['Cholesterol'] == 'above normal') & df['CVD Status'].isin(['negative'])])

    # Converts the above correlation into a new dataframe
    # smoker_cvd_correlation_2 = {"Status": ["CVD Negative", "CVD Positive"],
    #                             "Smokers": [smoker_neg_cvd, smoker_pos_cvd],
    #                             "Non Smokers": [non_smoker_neg_cvd, non_smoker_pos_cvd]
    #                             }

    smoker_cvd_correlation_2 = {"Status": ["CVD Negative", "CVD Positive"],
                                "Well Above": [smoker_neg_cvd, smoker_pos_cvd],
                                "Above": [non_smoker_neg_cvd, non_smoker_pos_cvd]
                                }

    # Heatmap showing relation between age and cholesterol levels
    fig = px.density_heatmap(df, x=age, y=cholesterol)

    # Scatter plot showing relation between height and weight levels
    fig2 = px.scatter(df, x=height, y=weight, color=cvd_status)

    # Figures for both pie charts. One each for smokers and non smokers
    # fig3 = px.pie(smoker_cvd_correlation_2, values="Non Smokers", names="Status", title="Non Smokers")
    # fig4 = px.pie(smoker_cvd_correlation_2, values="Smokers", names="Status", title="Smokers")

    fig3 = px.pie(smoker_cvd_correlation_2, values="Well Above", names="Status", title="Cholesterol WELL Above")
    fig4 = px.pie(smoker_cvd_correlation_2, values="Above", names="Status", title="Cholesterol Above")

    # Dash Layout
    dash_app.layout = html.Div(id='dash-container', children=[
        html.H1(children='List of data element cards'),

        html.H1(children='''
            Heat map of the relation between cholesterol level and age in the dataset.
        '''),
        dcc.Graph(
            id='heat_map',
            figure=fig,
            className='graphBox'
        ),

        html.H1(children='''
                Scatter plot of height as it relates to weight in the dataset.
            '''),
        dcc.Graph(
            id='scatter_plot',
            figure=fig2,
            className='graphBox'
        ),

        html.H1(children='''
                    Pie charts representing rates of CVD in smokers vs non smokers.
                '''),
        dcc.Graph(
            id='pie_graph_1',
            figure=fig3,
            className='graphBox'
        ),
        dcc.Graph(
            id='pie_graph_2',
            figure=fig4,
            className='graphBox'
        ),

        html.H1(children='''
                List of records
            '''),
        dash_table.DataTable(
            id='table',
            columns=[
                {"name": i, "id": i} for i in df.columns
            ],
            data=df[:20].to_dict('records'),
            style_cell_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
                'text-align': 'center'
            },

            css=[{
                'selector': '.dash-spreadsheet-container',
                'rule': 'border: 1px solid black; border-radius: 15px; overflow: hidden;'
            }]
        )
    ])
    return dash_app.server
