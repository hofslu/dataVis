"""
[Resouces]
    RangeSlider: https://community.plotly.com/t/dash-range-slider-with-date/17915/5 

"""

import dash
from dash import dcc, html, callback, Output, Input
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta


greenSpotify = 'rgb(30, 215, 96)'   # the official green spotify uses
# the official black spotify uses - for either only the user or the whole background
blackSpotify = 'rgb(25, 20, 20)'
# the other black - so its not so monotone
lightblackSpotify = 'rgb(41, 40, 40)'

# reading in the data
df = pd.read_csv("/home/johannes/Dokumente/tu/info_vis/dataVis/theAPP_copy/data/claras_songs.csv")

trackName = df["song_Name"]
artist = df["artist"]
timeStamp = df["TIME_STAMP"] 
timeStamp = pd.to_datetime(timeStamp)
timeStamp = timeStamp + timedelta(hours=2)   # adding 2 hours because the time is not right

BBscore = str(df["popularity"].mean())

### AB HIER BRAUCH ICH DAS NEUE DATAFRAME
# features = ["danceability", "liveness", "energy", "instrumentalness", "speechiness", "acoustiness"]
# mean_values_spider = df[features].mean()
mean_values_spider = [0.2,0.4,0.8, 0.5, 0.1, 0.1415]


# building the app
app = dash.Dash(__name__, external_stylesheets=['../static/css/test2.css'])

app.layout = html.Div([
    # Header
    html.Div(id = 'header', className = 'neonBox', children= 'Spotify User Dashboard'),
    # User Info
    html.Div(id='user-info', className='neonBox', children=[
        html.Div(id='info-header', className='neonText',
                 children='Clara Fall'),
        dcc.Input(id='my-input', value='initial value',
                  type='text'),  # dummy input
        html.Div(className='neonText', children='Basic bitch score:'),
        html.Div(id='bbScore', className='neonText', children=BBscore )
    ]),
    # Spider Chart
    html.Div(id='spider-chart', className='neonBox', children=[
        dcc.Graph(figure={}, id='spyder-graph')
    ]),
    # Song Info
    html.Div(id='song-info', className='neonBox')
    ,
    # Time Line
    html.Div(id='timeline', className='neonBox', children=[
        dcc.Graph(figure={}, id='timeline-graph')
    ])
])





# -------- Radar(Spider) Plot ----------------------------

def radarPlot(values):
    subjects = ["danceability", "liveness", "energy",
                "instrumentalness", "speechiness", "acoustiness"]

    df_radar = pd.DataFrame({'subjects': subjects, 'values': values})

    fig = px.line_polar(df_radar, r='values', theta='subjects',
                        line_close=True,
                        color_discrete_sequence=[greenSpotify])

    fig.update_traces(fill="toself")

    fig.update_polars(bgcolor=blackSpotify)

    fig.update_layout(
        autosize=True,
        height=None,
        width=None,
        polar=dict(
            radialaxis=dict(
                tickfont=dict(color='white'),
                tickvals=[0, 0.2, 0.4, 0.6, 0.8]
            ),
            angularaxis=dict(
                tickfont=dict(color='white')
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',  # this makes the background transparent
        plot_bgcolor='rgba(0,0,0,0)',
    )

    return fig


@callback(
    Output(component_id='spyder-graph', component_property='figure'),
    Input('my-input', 'value')
)
def update_spyder_graph(value):
    return radarPlot(mean_values_spider)




# -------- Time Plot ----------------------------


def timelineTracks(col_tracks, col_time, artist):
    df_timeline = pd.DataFrame({'col_time': col_time, 'col_tracks': col_tracks, 'artist': artist})

    fig = px.scatter(df_timeline, x='col_time', y=[0] * len(col_time),
                     title="Time Line of the last Songs you've listened to",
                     #hover_name='col_tracks' + ' - ' + 'artist',
                     hover_data={'col_time': False, 'col_tracks': False, 'artist': False},
                     color_discrete_sequence=[greenSpotify])

    fig.update_traces(marker=dict(size=15, opacity=0.6),
                      hovertemplate='<b>%{text}</b><br><br>%{x}',
                      text=df_timeline['col_tracks'] + " - " + df_timeline['artist'],
                      hoverlabel=dict(bgcolor=greenSpotify))

    fig.add_hline(y=0, line_color=greenSpotify)

    fig.update_xaxes(title_text=' ',
                     tickfont=dict(color='white'))

    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=10),
        hoverlabel=dict(
            font_size=13
        ),
        yaxis=dict(visible=False),
        showlegend=False,
        title_font=dict(color='white'),

        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',  # this makes the background transparent
    )

    return fig


@callback(
    Output(component_id='timeline-graph', component_property='figure'),
    Input('my-input', 'value')
)
def update_timeline_graph(value):
    return timelineTracks(trackName, timeStamp, artist)



if __name__ == '__main__':
    app.run_server(debug=False)
