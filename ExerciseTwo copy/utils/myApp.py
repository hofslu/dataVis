from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

from utils.WorldMap import build_world_map
from urllib.request import urlopen
import json


def build_app_layout(df):

    # parameters
    selection = ['Agricultural land (% of land area)', 'Agricultural land (sq. km)', 'Arable land (% of land area)', 'Arable land (hectares per person)', 'Arable land (hectares)', 'Birth rate, crude (per 1,000 people)', 'Death rate, crude (per 1,000 people)', 'GDP per capita (current US$)', 'Land area (sq. km)', 'Population, total', 'Rural population', 'Rural population (% of total population)', 'Rural population growth (annual %)', 'Surface area (sq. km)']
    county_codes = list(set(df['Country Code']))
    world_views = ['orthographic', 'natural earth']

    # get geo-json data 
    url = 'https://gist.githubusercontent.com/bquast/944781aa6dcc257ebf9aeee3c098b637/raw/871039f36e7b277a20d34619d72ec6b62957fe28/world-topo.json'
    with urlopen(url) as response:
        counties = json.load(response)
    
    # WorldFigure
    worldFfig = build_world_map(None, None)

    # App layout
    layout = dbc.Container([
        dbc.Row([
            html.H3("This is our first python dash(board) app :)", id='debug-line', style={'color': 'deeppink'})
        ]),

        dbc.Row([
            dbc.Col([
                    dbc.Row([
                        dcc.Dropdown(selection, selection[0], id='drop-down-country-attribute-item'),
                        dcc.RadioItems(world_views, world_views[0], id='drop-down-world-representation-item', style={'accent-color': 'pink'}),
                    ]),
                    dbc.Row([
                        # World-map
                        dcc.Graph(
                            figure=worldFfig, id='map-graph',
                            style={
                                'height': '425px',
                                }
                        )
                    ]),
            ]),
            dbc.Col(
                # Scatter-Plot
                dcc.Graph(figure={ }, id='scatter-graph',                     ######### clara aenderung index
                    style={
                        'height': '400px',
                    }),
                    width=6, 
                ),
        ], style={
            "height": "400px",
            "overflow": "hidden",
            }),
        dbc.Row([
            dbc.Col(
                # Time-Line
                dcc.Graph(figure={}, id='time-line-graph',
                style={
                    'height': '350px',
                    'width': '100%'
                }),
                width=6
                ),
        ], style={
            "display": "inline-block",
            "height": "350px",
            "width": "220%",
            })

    ],style={
        "height": "100vh", 
        "width": "100vw", 
        "overflow": "hidden",
        'boxsizing': 'border-box',
        'margin': '10px'
        })
    return layout
