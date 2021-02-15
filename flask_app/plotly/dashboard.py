import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import plotly.express as px
import pandas as pd

from model import convert_age_in_days_to_years


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
    cvd_status = df['CVD Status']

    fig = px.density_heatmap(df, x=age, y=cvd_status)
    fig2 = px.box(df, x=age, y=cholesterol)
    fig3 = px.line(df, x=age, y=cholesterol)

    # Create Dash Layout
    # dash_app.layout = html.Div(id='dash-container')
    dash_app.layout = html.Div(id='dash-container', children=[
        html.H1(children='List of data element cards'),

        html.H1(children='''
            Heat map
            Cholesterol correlated to age:
        '''),

        dcc.Graph(
            id='graph',
            figure=fig,
            className='graphBox'
        ),

        html.H1(children='''
                Next graph.
            '''),

        dcc.Graph(
            id='example-graph-2',
            figure=fig2,
            className='graphBox'
        ),

        html.H1(children='''
                    Next graph.
                '''),

        dcc.Graph(
            id='example-graph-3',
            figure=fig3,
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
