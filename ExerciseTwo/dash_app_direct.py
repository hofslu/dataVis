from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px


from utils.PrincipalComponentAnalysis import PrComAnalysis
from utils.WorldMap import build_world_map
from utils.myApp import build_app_layout

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

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = build_app_layout(df)

import plotly.express as px
import plotly.graph_objs as go
import pandas as pd



# Add controls to build the interaction
@callback(
    Output(component_id='map-graph', component_property='figure'),
    Input(component_id='drop-down-world-representation-item', component_property='value')
)
def update_map(style):
    return build_world_map(style)


# Add controls to build the interaction
@callback(
    Output(component_id='scatter-graph', component_property='figure'),
    Input(component_id='drop-down-country-attribute-item', component_property='value')
)
def update_graph(col_chosen):
    df_PCA = PrComAnalysis(df, col_chosen)          ####    clara aenderung
    fig = px.scatter(df_PCA, x=df_PCA['PC1'], y=df_PCA['PC2'], 
                     title = "PCA -" + col_chosen,
                     hover_name='Country Code',
                     hover_data = {'PC1': False, 'PC2':False})      #### clara aenderung

    fig.update_traces(marker=dict(size= 15, color='lightpink', opacity=0.6))

    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=10),
        hoverlabel=dict(
        font_size=13
        )  
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
    fig = px.line(df, x=df['year'][start:end], y=df[attr_chosen].iloc[start:end], 
                  title=country_chosen + " - " + attr_chosen, 
                  labels={
                     'x': "Year",
                     'y': attr_chosen})         #### clara aenderung
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
    fig.update_traces(line_color='lightpink')           #### clara aenderung
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
