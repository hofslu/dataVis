"""
[Resouces]
    RangeSlider: https://community.plotly.com/t/dash-range-slider-with-date/17915/5 

"""

import dash
from dash import dcc, html, callback, Output, Input, State
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta

from scripts.utils import get_df


greenSpotify = 'rgb(30, 215, 96)'   # the official green spotify uses
# the official black spotify uses - for either only the user or the whole background
blackSpotify = 'rgb(25, 20, 20)'
# the other black - so its not so monotone
lightblackSpotify = 'rgb(41, 40, 40)'

# reading in the data
# df = pd.read_csv("/Users/clarapichler/Desktop/SS 2023/Informationsvisualisierung/dataVis/theAPP_copy/claras_songs.csv")

LUKAS_CLIENT_ID = "207e1c72689d4a0a88e0e721cb9bb254"
LUKAS_CLIENT_SECRET = "2b98d70fb10b4ca1b0008405a353d35c"

CLARA_CLIENT_ID = "b8db48d0784f4e2b9ab719adc118e918"
CLARA_CLIENT_SECRET = "0a7feca73df44f1c829f125dbe8a6b91"

df = get_df(CLARA_CLIENT_ID, CLARA_CLIENT_SECRET)

trackName = [df["song_Name"], df["song_Name"]]
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
    html.Div(id='header', className='neonBox',
             children='Spotify User Dashboard'),
    # User Info
    html.Div(id='user-info', className='neonBox', children=[
        html.Div(id='info-header', className='neonText',
                 children='Clara Fall'),
        dcc.Input(id='my-input', value='initial value',
                  type='text'),  # dummy input
        html.Div(className='neonText', children='Basic bitch score:'),
        html.Div(id='bbScore', className='neonText', children=BBscore)
    ]),
    # Spider Chart
    html.Div(id='spider-chart', className='neonBox', children=[
        dcc.Graph(figure={}, id='spyder-graph')

    ]),
    # Song Info
    html.Div(id='song-info', className='neonBox'),

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
                        color_discrete_sequence=px.colors.sequential.Plasma_r)

    if values2 is not None:
        # pass
        df_radar2 = pd.DataFrame({'subjects': subjects, 'values': values2})
        fig.add_trace(px.line_polar(df_radar2, r=values, theta=subjects,
                                    line_close=True,
                                    color_discrete_sequence=["green"]))

    fig.update_traces(fill="toself")
    fig.update_layout(showlegend=False)

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
    Input('timeline-graph', 'clickData')
)
def update_spyder_graph(click_data):
    # print(click_data)
    if click_data is None:
        return radarPlot(mean_values_spider, None)

    point_index = click_data['points'][0]['pointIndex']

    song_features = df.iloc[point_index][features]

    return radarPlot(mean_values_spider, song_features)


# -------- Time Plot ----------------------------


def timelineTracks(col_tracks, col_time, artist):
    df_timeline = pd.DataFrame({'col_time': col_time, 'col_tracks': col_tracks, 'artist': artist})

    fig = px.scatter(df_timeline, x='col_time', y='dummy', color = 'dummy',
                     title="Time Line of the last Songs you've listened to",
                     #hover_name='col_tracks' + ' - ' + 'artist',
                     hover_data={'col_time': False, 'col_tracks': False, 'artist': False},
                     color_discrete_sequence=[greenSpotify])

    fig.update_traces(marker=dict(size=15, opacity=0.6),
                      hovertemplate='<b>%{text}</b><br><br>%{x}',
                      text=df_timeline['col_tracks'] +
                      " - " + df_timeline['artist'],
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
    Input('timeline-graph', 'value')
)
def update_timeline_graph(value):
    return timelineTracks(trackName, timeStamp, artist)


# # -------- Song Info ----------------------------

@app.callback(
    Output('song-info', 'children'),
    Input('timeline-graph', 'clickData')
)
def update_song_info(click_data):
    if click_data is not None:
        point_index = click_data['points'][0]['pointIndex']
        track_info = str(trackName[point_index]) + \
            " by " + str(artist[point_index])

        return html.Div([
            html.Div(id='song-box', className='neonText',
                     children='Song Information'),
            html.Div(id='selected-song', className='neonText',
                     children=track_info)
        ])

    return html.Div([
        html.Div(id='song-box', className='neonText',
                 children='Song Information'),
        html.Div(id='selected-song', className='neonText',
                 children="Please select a Song in\nthe Time Line")
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
