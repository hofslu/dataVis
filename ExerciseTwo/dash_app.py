
from dash import Dash, html, dash_table, dcc, callback, Output, Input

import dash_bootstrap_components as dbc
import plotly.express as px

import pandas as pd

import os

# load data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
# for i in range(0,4):
#     name = 'new_col_' + str(i)
#     df[name] = 1


# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)


# App layout
app.layout = dbc.Container([
    # dbc.Row([
    #     html.H1("This is our first python dash(board) app :)")
    # ]),

    dbc.Row([
        dbc.Col([
                dbc.Row([
                    dcc.Dropdown(['pop', 'lifeExp', 'gdpPercap'], 'lifeExp', id='controls-and-radio-item'),
                ]),
                dbc.Row([
                    # World-map
                    dcc.Graph(
                        figure={}, id='map-graph',
                        style={'height': '325px'}
                    )
                ]),
        ]),
        dbc.Col(
            # Scatter-Plot
            dcc.Graph(figure={}, id='scatter-graph',
                style={
                    # "background-color": "#ADD8E6",
                    'height': '350px'
                }),
                width=6, 
            ),
    ], style={
        "height": "350px",
        "overflow": "hidden"
        }),
    dbc.Row([
        dbc.Col(
            # Time-Line
            dcc.Graph(figure={}, id='time-line-graph',
            style={
                'height': '375px'
            }),
            width=6, style={
                # "background-color": "#D8BFD8",
                }
            ),
        dbc.Col(
            # detailed-information
            dash_table.DataTable(data=df.to_dict('records'), 
            page_size=10
            ),
            width=6,
            ),
    ], style={
        "height": "350px",
        # "overflow": "hidden"
        })

],style={
    "height": "100vh", 
    "width": "100vw", 
    # "background-color": "wheat",
    "overflow": "hidden",
    })
        # html.Div([
        #     # html.Div(children='My First App with Data, Graph, and Controls'),
        #     # html.Hr(),
        #     dcc.Dropdown(['pop', 'lifeExp', 'gdpPercap', 'new_col_2'], 'lifeExp', id='controls-and-radio-item'),
        #     dash_table.DataTable(data=df.to_dict('records'), page_size=10),
        #     dcc.Graph(figure={}, id='map-graph'),
        #     dcc.Graph(figure={}, id='scatter-graph'),
        #     dcc.Graph(figure={}, id='controls-and-graph')
        # ])




# Add controls to build the interaction
@callback(
    Output(component_id='map-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    fig.update_layout(margin=dict(l=0, r=0, t=5, b=0))
    return fig


# Add controls to build the interaction
@callback(
    Output(component_id='scatter-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.scatter(df, x='continent', y='continent')
    fig.update_layout(margin=dict(l=0, r=0, t=10, b=10))
    return fig


# Add controls to build the interaction
@callback(
    Output(component_id='time-line-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.line(df, x=df.index, y=col_chosen) #, title=col_chosen)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
