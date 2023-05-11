import plotly.express as px
import plotly.graph_objects as go

import pandas as pd



def build_world_map(df, style='orthographic'):
    from urllib.request import urlopen
    import json
    url = 'https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'
    # url = 'https://gist.githubusercontent.com/bquast/944781aa6dcc257ebf9aeee3c098b637/raw/871039f36e7b277a20d34619d72ec6b62957fe28/world-topo.json'
    with urlopen(url) as response:
        counties = json.load(response)
        print(json.dumps(counties, indent=2))

    # import pandas as pd
    # df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
    #                 dtype={"fips": str})

    import plotly.express as px

    fig = px.choropleth(df, geojson=counties,
        color_continuous_scale="Viridis",
        range_color=(0, 12),
        scope="usa",
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


def build_world_map_org(style='orthographic'):
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

    # worldFfig.add_trace(go.Scattergeo(lon=df["longitude"],
    #             lat=df["latitude"],
    #             text=df["data"],
    #             textposition="middle center",
    #             mode='text',
    #             showlegend=False))

    worldFfig = go.Figure(go.Scattergeo())
    worldFfig.update_geos(projection_type=style)
    worldFfig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})

    return worldFfig
