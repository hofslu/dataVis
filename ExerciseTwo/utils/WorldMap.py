import plotly.express as px
import plotly.graph_objects as go

from urllib.request import urlopen

import pandas as pd

import json

def dev_build_world_map():
    url = 'https://gist.githubusercontent.com/bquast/944781aa6dcc257ebf9aeee3c098b637/raw/871039f36e7b277a20d34619d72ec6b62957fe28/world-topo.json'
    with urlopen(url) as response:
        counties = json.load(response)

    fig = px.choropleth(
        geojson=counties,
        locations=['AUT', 'USA', 'DEU'], 
        locationmode="ISO-3", 
        color=[1, 1, 1],
        # scope="usa"
        )
    
    return fig

def build_world_map(df, geojson, style='orthographic'):


    fig = px.choropleth(
        locations=["Austria"], 
        locationmode="country names", 
        color=[1], 
        # df, geojson=geojson,
        # color_continuous_scale="Viridis",
        # range_color=(0, 12),
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


def build_world_map_tutorial(style='orthographic'):
    # drop-down-world-representation-item
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

    worldFfig = go.Figure(go.Scattergeo())
    worldFfig.update_geos(projection_type=style)
    worldFfig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})

    return worldFfig



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

