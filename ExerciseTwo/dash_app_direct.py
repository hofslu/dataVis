
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.graph_objects as go

import dash_bootstrap_components as dbc
import plotly.express as px

from utils.PrincipalComponentAnalysis import PrComAnalysis

import pandas as pd

import os



def build_map_from_df(df):
    fig = 'Choropleth-Map'
    return fig

def build_tooltip(df, selection):
    tooltip = {
        "attributeOne": 1,
        "attributeTwo": 2,
        "attributeString": "Information",
    }
    return tooltip


def build_time_line(df, selection):
    """builds dataframe for time-series representation

    Args:
        df (Pandas.DataFrame): full data-frame
        selection (string): Country Code

    Returns:
        Pandas.DataFrame: head(Year, selection)
    """
    return 



# -----------------------------------------------------------------------------------


# load data
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = pd.read_csv('./data/preproc_claras_dataframe.csv')

selection = ['Agricultural land (% of land area)', 'Agricultural land (sq. km)', 'Arable land (% of land area)', 'Arable land (hectares per person)', 'Arable land (hectares)', 'Birth rate, crude (per 1,000 people)', 'Death rate, crude (per 1,000 people)', 'GDP per capita (current US$)', 'Land area (sq. km)', 'Population, total', 'Rural population', 'Rural population (% of total population)', 'Rural population growth (annual %)', 'Surface area (sq. km)']
county_codes = list(set(df['Country Code']))

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

worldFfig = go.Figure(go.Scattergeo())
worldFfig.update_geos(projection_type="orthographic")
worldFfig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})


import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

def get_world_plot():
    rows=[['501-600','15','122.58333','45.36667'],
        ['till 500','4','12.5','27.5'],
        ['more 1001','41','-115.53333','38.08'],
        ]
    colmns=['bins','data','longitude','latitude']
    df=pd.DataFrame(data=rows, columns=colmns)
    df = df.astype({"data": int})

    worldFfig=px.scatter_geo(df,lon='longitude', 
        lat='latitude',
        color='bins',
        opacity=0.5,
        size='data',
        projection="orthographic", 
        hover_data=(['bins'])
        )

    # worldFfig.add_trace(go.Scattergeo(lon=df["longitude"],
    #             lat=df["latitude"],
    #             text=df["data"],
    #             textposition="middle center",
    #             mode='text',
    #             showlegend=False))
    return worldFfig
worldFfig = get_world_plot()


# App layout
app.layout = dbc.Container([
    # dbc.Row([
    #     html.H1("This is our first python dash(board) app :)")
    # ]),

    dbc.Row([
        dbc.Col([
                dbc.Row([
                    # dcc.Dropdown(county_codes, county_codes[0], id='drop-down-country-code-item'),
                    dcc.Dropdown(selection, selection[0], id='drop-down-country-attribute-item'),
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



# Add controls to build the interaction
# @callback(
#     Output(component_id='map-graph', component_property='figure'),
#     # Input(component_id='drop-down-country-attribute-item', component_property='value')
# )
# def update_graph(col_chosen):
#     # fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
#     fig = go.Figure(go.Scattergeo())
#     fig.update_geos(projection_type="orthographic")
#     fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
#     return fig


# Add controls to build the interaction
@callback(
    Output(component_id='scatter-graph', component_property='figure'),
    Input(component_id='drop-down-country-attribute-item', component_property='value')
)
def update_graph(col_chosen):
    df_PCA = PrComAnalysis(df, col_chosen)          ####    clara aenderung
    fig = px.scatter(df_PCA, x=df_PCA['PC1'], y=df_PCA['PC2'], 
                     title = "PrincipalComponantAnalysis - " + col_chosen,
                     hover_data={'Country Code':True,
                                 'PC1':False,
                                 'PC2': False})      #### clara aenderung
    fig.update_layout(
        margin=dict(l=30, r=30, t=60, b=10),
        )
    return fig


# Add controls to build the interaction
@callback(
    Output(component_id='time-line-graph', component_property='figure'),
    Input(component_id='drop-down-country-code-item', component_property='value'),
    Input(component_id='drop-down-country-attribute-item', component_property='value')
)
def update_graph(country_chosen, attr_chosen):
    indices = df.index[df['Country Code'] == country_chosen].tolist()
    start = min(indices)
    end = max(indices)
    # x, y = from_function(df)
    fig = px.line(df, x=df['year'][start:end], y=df[attr_chosen].iloc[start:end], title=country_chosen + " - " + attr_chosen)
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
