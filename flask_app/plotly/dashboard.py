import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/css/data.css',
            dbc.themes.BOOTSTRAP
        ]
    )

    # Columns: Age, Height, Weight, Gender, Systolic BP, Diastolic BP,
    #           Cholesterol, Glucose, Smoking, Alcohol Intake, Physical Activity
    df = pd.read_csv("flask_app/static/data/readable_cvd_data.csv")
    cholesterol = df['Cholesterol']
    height = df['Height (cm)']
    weight = df['Weight (kg)']
    bmi = df['BMI']
    cvd_status = df['CVD Status']
    smoker_status = df['Smoker']

    importance_df = pd.read_csv('flask_app/static/data/importance_dataset.csv')

    # Retrieves smoker data from the imported dataframe and correlates it to whether the patient/user is a smoker
    smoker_pos_cvd = len(df[(smoker_status == 'yes') & cvd_status.isin(['positive'])])
    smoker_neg_cvd = len(df[(smoker_status == 'yes') & cvd_status.isin(['negative'])])
    non_smoker_pos_cvd = len(df[(smoker_status == 'no') & cvd_status.isin(['positive'])])
    non_smoker_neg_cvd = len(df[(smoker_status == 'no') & cvd_status.isin(['negative'])])

    cholesterol_well_above_pos_cvd = len(df[(cholesterol == 'well above normal') & cvd_status.isin(['positive'])])
    cholesterol_well_above_neg_cvd = len(df[(cholesterol == 'well above normal') & cvd_status.isin(['negative'])])
    cholesterol_above_pos_cvd = len(df[(cholesterol == 'above normal') & cvd_status.isin(['positive'])])
    cholesterol_above_neg_cvd = len(df[(cholesterol == 'above normal') & cvd_status.isin(['negative'])])
    cholesterol_normal_pos_cvd = len(df[(cholesterol == 'normal') & cvd_status.isin(['positive'])])
    cholesterol_normal_neg_cvd = len(df[(cholesterol == 'normal') & cvd_status.isin(['negative'])])

    importance_bar_graph_figure = px.bar(importance_df.sort_values(by=['Importance']), x='Importance',
                                         y='Variable',
                                         title='Health variables importance relative to determining the likelihood of '
                                               'testing positive for CVD')

    # Scatter plot showing relation between height and weight levels
    height_and_weight_scatter_plot = px.scatter(df, x=height, y=weight, size=bmi, color=cvd_status,
                                                title='Height as it relates to weight and BMI')

    subplots_for_cholesterol_pie_charts = make_subplots(rows=1, cols=3,
                                                        specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]])

    cholesterol_well_above_pie_chart = go.Pie(title="Cholesterol WELL Above Normal",
                                              labels=['CVD Positive', 'CVD Negative'],
                                              values=[cholesterol_well_above_pos_cvd, cholesterol_well_above_neg_cvd]
                                              )

    cholesterol_above_pie_chart = go.Pie(title="Cholesterol Above Normal",
                                         labels=['CVD Positive', 'CVD Negative'],
                                         values=[cholesterol_above_pos_cvd, cholesterol_above_neg_cvd]
                                         )

    cholesterol_normal_pie_chart = go.Pie(title="Cholesterol Normal",
                                          labels=['CVD Positive', 'CVD Negative'],
                                          values=[cholesterol_normal_pos_cvd, cholesterol_normal_neg_cvd]
                                          )

    subplots_for_cholesterol_pie_charts.append_trace(cholesterol_well_above_pie_chart, row=1, col=1)
    subplots_for_cholesterol_pie_charts.append_trace(cholesterol_above_pie_chart, row=1, col=2)
    subplots_for_cholesterol_pie_charts.append_trace(cholesterol_normal_pie_chart, row=1, col=3)
    subplots_for_cholesterol_pie_charts.update_layout(title_text="Cholesterol level correlation to CVD status")

    subplots_for_smoking_status = make_subplots(rows=1, cols=2,
                                                specs=[[{"type": "pie"}, {"type": "pie"}]])

    smoker_pie_chart = go.Pie(title="Smoker",
                              labels=['CVD Positive', 'CVD Negative'],
                              values=[smoker_pos_cvd, smoker_neg_cvd]
                              )

    non_smoker_pie_chart = go.Pie(title="Noon Smoker",
                                  labels=['CVD Positive', 'CVD Negative'],
                                  values=[non_smoker_pos_cvd, non_smoker_neg_cvd]
                                  )

    subplots_for_smoking_status.append_trace(smoker_pie_chart, row=1, col=1)
    subplots_for_smoking_status.append_trace(non_smoker_pie_chart, row=1, col=2)
    subplots_for_smoking_status.update_layout(title_text="Smoking status correlation to CVD status")

    # Dash dashboard layout
    dash_app.title = "Dataset"
    dash_app.layout = html.Div(id='dash-container', children=[

        # Bootstrap navbar
        html.Div(children=[
            html.Nav(className="navbar navbar-expand-lg navbar-light bg-light", children=[
                html.Div(className="collapse navbar-collapse", id="navbarSupportedContent", children=[
                    html.Ul(className="navbar-nav mr-auto", children=[
                        html.Li(className="nav-item active", children=[
                            html.A("Enter Vitals", className="nav-link", href="/determine_risk")
                        ]),
                        html.Li(className="nav-item", children=[
                            html.A("Dataset", className="nav-link", href="#")
                        ])
                    ]),
                    html.A("Logout", className="nav-link", href="/logout")
                ])
            ]),
        ]),

        html.Br(),
        html.H1('List of analysed data elements:'),
        # Horizontal bar graph for feature importance
        dcc.Graph(
            id='bar_graph',
            figure=importance_bar_graph_figure,
            className='graphBox'
        ),

        html.Br(),
        # Scatter plot for height and weight correlation
        dcc.Graph(
            id='scatter_plot',
            figure=height_and_weight_scatter_plot,
            className='graphBox'
        ),

        html.Br(),
        # Pie charts for cholesterol correlation
        dcc.Graph(
            id='pie_graph_set_1',
            figure=subplots_for_cholesterol_pie_charts,
            className='graphBox'
        ),
        # Pie charts for smoking correlation
        dcc.Graph(
            id='pie_graph_set_2',
            figure=subplots_for_smoking_status,
            className='graphBox'
        ),

        html.Br(),
        html.H1("List of Records"),
        # Displays head of dataset in readable format
        dash_table.DataTable(
            id='table',
            columns=[
                {"name": i, "id": i} for i in df.columns
            ],
            # title='Records',
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
