from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import time

import plotly.graph_objs as go

from utils.PrincipalComponentAnalysis import PrComAnalysis
from utils.WorldMap import build_world_map, dev_build_world_map, build_world_map_tutorial
build_world_map = dev_build_world_map
# build_world_map = build_world_map_tutorial
from utils.myApp import build_app_layout
# from utils.CallbackLinks import *

import pandas as pd
import os


# load data
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = pd.read_csv('./data/preproc_claras_dataframe.csv')
df = df.drop(0)

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = build_app_layout(df)





# -------------------------------------------------------------------------------------------------------------------------
# ----------------- Callback Links ----------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------

# -------- World Map ----------------------------
@callback(
    Output(component_id='map-graph', component_property='figure'),
    [Input(component_id='drop-down-world-representation-item', component_property='value'),
    Input(component_id='scatter-graph', component_property='hoverData'),
    Input(component_id='map-graph', component_property='hoverData')]
)
def update_map(style, hover_scatter, hover_map):
    time.sleep(0.01)
    fig =  build_world_map(hover_scatter, hover_map, style)
    return fig


# -------- Scatter Plot ----------------------------
@callback(
    Output(component_id='scatter-graph', component_property='figure'),
    [Input(component_id='drop-down-country-attribute-item', component_property='value'),
    Input(component_id='scatter-graph', component_property='hoverData'),
    Input(component_id='map-graph', component_property='hoverData')]
)
def update_scatter(col_chosen, hover_scatter, hover_map):
    print(hover_map)
    print(hover_scatter)
    time.sleep(0.01)
    country = None
    print(hover_scatter)
    print(hover_map)
    if hover_scatter:
        country = hover_scatter['points'][0]['hovertext']
    elif hover_map:
        country = hover_map['points'][0]['location']
    else:
        pass
    df_PCA = PrComAnalysis(df, col_chosen)          ####    clara aenderung
    df_PCA = pd.concat([df_PCA, df_PCA['Country Code'] == country], axis = 1)
    df_PCA.columns = ['PC1', 'PC2', 'Country Code', 'chosen']
    df_PCA = df_PCA.sort_values(by = 'chosen')

    fig = px.scatter(df_PCA, x=df_PCA['PC1'], y=df_PCA['PC2'], 
                     title = "PrincipalCompnentAnalysis - " + col_chosen,
                     hover_name='Country Code',
                     hover_data = {'PC1': False, 'PC2':False, 'chosen':False},
                     color = 'chosen',
                     color_discrete_sequence = ['pink', 'deeppink'])    #### clara aenderung

    fig.update_traces(marker=dict(size= 15, opacity=0.6))
    #fig.update_layout()
    #fig.update_traces(marker_showscale=False)
    #fig.update_traces(marker_coloraxis=None)
    #fig.update_layout(coloraxis_showscale=False)
    #fig.update_coloraxes(showscale=False)
    #fig.update(layout_coloraxis_showscale=False)

    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=10),
        hoverlabel=dict(
        font_size=13
        )  
    )
    fig.update_layout(showlegend=False)
    return fig


# -------- Time Series -----------------------------
@callback(
    Output(component_id='time-line-graph', component_property='figure'),
    [Input(component_id='map-graph', component_property='clickData'),
    Input(component_id='drop-down-country-attribute-item', component_property='value')]
    # Input(component_id='scatter-graph', component_property='clickData'),
    # Input(component_id='drop-down-country-code-item', component_property='value'),
)
def update_time_line(country_chosen, attr_chosen):
    # country_chosen = country_chosen['points'][0]['hovertext'] # scatter plot change
    if country_chosen is None: 
        fig = px.line(x=[0,1], y=[1,1])
        fig.update_traces(line_color='pink')           #### clara aenderung
    else: 
        country_chosen = country_chosen['points'][0]['location'] # world map change

        indices = df.index[df['Country Code'] == country_chosen].tolist()
        start = min(indices)
        end = max(indices)
        
        line_df = df.iloc[start:end]
        print(df.columns.values)
        fig = px.line(line_df, 
            x=line_df['year'], 
            y=line_df[attr_chosen],
            title=country_chosen + " - " + attr_chosen, 
            labels={
                'x': "Year",
                'y': attr_chosen},
            # hover_name=attr_chosen,
            hover_data={'year':False}
            )         #### clara aenderung
        fig.update_traces(line_color='deeppink')           #### clara aenderung


    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
    return fig



# # -------- Header ----------------------------------
# @callback(
#     Output(component_id='debug-line', component_property='children'),
#     Input(component_id='scatter-graph', component_property='clickData')
# )
# def update_debug_line(data):
#     print(data)

# reset hoverData for scatter
@callback(
    Output(component_id='scatter-graph', component_property='hoverData'),
    Input(component_id='map-graph', component_property='hoverData')
)
def reset_hover_scatter(hover_map):
    return None




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
