from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

from utils.WorldMap import build_world_map

def build_app_layout(df):

    # parameters
    selection = ['Agricultural land (% of land area)', 'Agricultural land (sq. km)', 'Arable land (% of land area)', 'Arable land (hectares per person)', 'Arable land (hectares)', 'Birth rate, crude (per 1,000 people)', 'Death rate, crude (per 1,000 people)', 'GDP per capita (current US$)', 'Land area (sq. km)', 'Population, total', 'Rural population', 'Rural population (% of total population)', 'Rural population growth (annual %)', 'Surface area (sq. km)']
    county_codes = list(set(df['Country Code']))
    world_views = ['orthographic', 'natural earth']

    # WorldFigure
    worldFfig = build_world_map(df)

    # App layout
    layout = dbc.Container([
        # dbc.Row([
        #     html.H1("This is our first python dash(board) app :)")
        # ]),

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
            dcc.Dropdown(county_codes, county_codes[0], id='drop-down-country-code-item'),
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