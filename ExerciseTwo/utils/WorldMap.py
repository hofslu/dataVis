import plotly.express as px
import plotly.graph_objects as go

from urllib.request import urlopen

import pandas as pd

import json

def build_world_map(hover_scatter, hover_map, style='orthographic'):
    url = 'https://gist.githubusercontent.com/bquast/944781aa6dcc257ebf9aeee3c098b637/raw/871039f36e7b277a20d34619d72ec6b62957fe28/world-topo.json'
    with urlopen(url) as response:
        counties = json.load(response)

    data = pd.read_csv('./data/preproc_claras_dataframe.csv')

    country = None
    if hover_scatter:
        country = hover_scatter['points'][0]['hovertext']
    elif hover_map:
        country = hover_map['points'][0]['location']
    else:
        pass
    
    countries = pd.Series(data['Country Code'].unique())
    colors = pd.Series(countries == country)
    df = pd.concat([countries, colors], axis = 1)
    df.columns = ['countries', 'color']
    df = df.sort_values(by = 'color')

    fig = px.choropleth(df,
        geojson=counties,
        locations='countries', 
        locationmode="ISO-3", 
        color='color',
        projection=style,
        color_discrete_sequence = ['pink', 'deeppink'],

        hover_name ='countries',
        hover_data={'countries': False, 'color':False}
        )
    fig.update_layout(
        showlegend=False,
        hoverlabel={
            'font_size': 13,
            'bgcolor': 'deeppink'
        }
        )    
    return fig


if __name__ == "__main__":
    from dash import Dash, html, dash_table, dcc, callback, Output, Input
    import dash_bootstrap_components as dbc

    external_stylesheets = [dbc.themes.CERULEAN]
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    worldFfig = dev_build_world_map()
    app.layout = dbc.Container([
        dcc.Graph(
            figure=worldFfig, id='map-graph',
            style={
                'height': '425px',
                }
        )
    ])
    app.run_server(debug=True)

