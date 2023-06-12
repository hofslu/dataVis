from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

from utils.WorldMap import build_world_map, dev_build_world_map, build_world_map_tutorial
build_world_map = dev_build_world_map
# build_world_map = build_world_map_tutorial
from urllib.request import urlopen
import json


def build_app_layout(df):

    # parameters
    selection = ['Agricultural land (% of land area)', 'Agricultural land (sq. km)', 'Arable land (% of land area)', 'Arable land (hectares per person)', 'Arable land (hectares)', 'Birth rate, crude (per 1,000 people)', 'Death rate, crude (per 1,000 people)', 'GDP per capita (current US$)', 'Land area (sq. km)', 'Population, total', 'Rural population', 'Rural population (% of total population)', 'Rural population growth (annual %)', 'Surface area (sq. km)']
    county_codes = list(set(df['Country Code']))
    world_views = ['orthographic', 'natural earth']

    # get geo-json data 
    # url = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'
    url = 'https://gist.githubusercontent.com/bquast/944781aa6dcc257ebf9aeee3c098b637/raw/871039f36e7b277a20d34619d72ec6b62957fe28/world-topo.json'
    with urlopen(url) as response:
        counties = json.load(response)

    # import pandas as pd
    # df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
    #                 dtype={"fips": str})
    
    # WorldFigure
    worldFfig = build_world_map(None, None)

    # App layout
    layout = dbc.Container([
        dbc.Row([
            html.H1(" ", id='debug-line')
        ]),

        dbc.Row([
            dbc.Col([
                    dbc.Row([
                        # dcc.Dropdown(county_codes, county_codes[0], id='drop-down-country-code-item'),
                        dcc.Dropdown(selection, selection[0], id='drop-down-country-attribute-item'),
                        dcc.RadioItems(world_views, world_views[0], id='drop-down-world-representation-item'),
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
                        # "background-color": "#ADD8E6",
                        'height': '400px',
                        'width': 'auto'
                    }),
                    width=6, 
                ),
        ], style={
            "height": "400px",
            "overflow": "hidden"
            }),
        dbc.Row([
            # dcc.Dropdown(county_codes, county_codes[0], id='drop-down-country-code-item'),
            dbc.Col(
                # Time-Line
                dcc.Graph(figure={}, id='time-line-graph',
                style={
                    'height': '350px',
                    'width': 'auto'
                }),
                width=6, style={
                    # "background-color": "#D8BFD8",
                    }
                ),
        ], style={
            "display": "inline-block",
            "height": "350px",
            "width": "200%",
            # "overflow": "hidden"
            })

    ],style={
        "height": "100vh", 
        "width": "100vw", 
        # "background-color": "wheat",
        "overflow": "hidden",
        })
    return layout
