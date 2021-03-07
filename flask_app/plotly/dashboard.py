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

    fig = px.bar(importance_df.sort_values(by=['Importance']), x='Importance',
                 y='Variable',
                 title='Health variables importance relative to determining the likelihood of testing positive for CVD')

    # Scatter plot showing relation between height and weight levels
    fig2 = px.scatter(df, x=height, y=weight, color=cvd_status, title='Height as it relates to weight')

    fig345 = make_subplots(rows=1, cols=3,
                           specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]])

    fig3 = go.Pie(title="Cholesterol WELL Above Normal",
                  labels=['CVD Positive', 'CVD Negative'],
                  values=[cholesterol_well_above_pos_cvd, cholesterol_well_above_neg_cvd]
                  )

    fig4 = go.Pie(title="Cholesterol Above Normal",
                  labels=['CVD Positive', 'CVD Negative'],
                  values=[cholesterol_above_pos_cvd, cholesterol_above_neg_cvd]
                  )

    fig5 = go.Pie(title="Cholesterol Normal",
                  labels=['CVD Positive', 'CVD Negative'],
                  values=[cholesterol_normal_pos_cvd, cholesterol_normal_neg_cvd]
                  )

    fig345.append_trace(fig3, row=1, col=1)
    fig345.append_trace(fig4, row=1, col=2)
    fig345.append_trace(fig5, row=1, col=3)
    fig345.update_layout(title_text="Cholesterol level correlation to CVD status")

    fig56 = make_subplots(rows=1, cols=2,
                          specs=[[{"type": "pie"}, {"type": "pie"}]])

    fig5 = go.Pie(title="Smoker",
                  labels=['CVD Positive', 'CVD Negative'],
                  values=[smoker_pos_cvd, smoker_neg_cvd]
                  )

    fig6 = go.Pie(title="Noon Smoker",
                  labels=['CVD Positive', 'CVD Negative'],
                  values=[non_smoker_pos_cvd, non_smoker_neg_cvd]
                  )

    fig56.append_trace(fig5, row=1, col=1)
    fig56.append_trace(fig6, row=1, col=2)
    fig56.update_layout(title_text="Smoking status correlation to CVD status")

    # Dash Layout
    dash_app.layout = html.Div(id='dash-container', children=[

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
                    html.Form(className="form-inline my-2 my-lg-0", children=[
                        html.Button("Logout", className="btn btn-outline-success my-2 my-sm-0", type="submit",
                                    id="logoutButton")
                    ])
                ])
            ]),
        ]),

        html.Br(),
        html.H1('List of analysed data elements:'),
        dcc.Graph(
            id='heat_map',
            figure=fig,
            className='graphBox'
        ),

        html.Br(),
        dcc.Graph(
            id='scatter_plot',
            figure=fig2,
            className='graphBox'
        ),

        html.Br(),
        dcc.Graph(
            id='pie_graph_set_1',
            figure=fig345,
            className='graphBox'
        ),
        dcc.Graph(
            id='pie_graph_set_2',
            figure=fig56,
            className='graphBox'
        ),

        html.Br(),
        html.H1("List of Records"),
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
