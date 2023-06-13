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
import numpy as np

from scripts.utils import get_df


greenSpotify = 'rgb(30, 215, 96)'   # the official green spotify uses
# the official black spotify uses - for either only the user or the whole background
blackSpotify = 'rgb(25, 20, 20)'
# the other black - so its not so monotone
lightblackSpotify = 'rgb(41, 40, 40)'



LUKAS_CLIENT_ID = "207e1c72689d4a0a88e0e721cb9bb254"
LUKAS_CLIENT_SECRET = "2b98d70fb10b4ca1b0008405a353d35c"

CLARA_CLIENT_ID = "b8db48d0784f4e2b9ab719adc118e918"
CLARA_CLIENT_SECRET = "0a7feca73df44f1c829f125dbe8a6b91"

#df = get_df(CLARA_CLIENT_ID, CLARA_CLIENT_SECRET)

df_clara = pd.read_csv("/home/johannes/Dokumente/tu/info_vis/dataVis/theAPP_copy/data/claras_songs.csv")
df_lukas = pd.read_csv("/home/johannes/Dokumente/tu/info_vis/dataVis/theAPP_copy/data/claras_songs.csv")
df_johannes = pd.read_csv("/home/johannes/Dokumente/tu/info_vis/dataVis/theAPP_copy/data/claras_songs.csv")
dict_df = {'Clara': df_clara, 'Lukas': df_lukas, 'Johannes':df_johannes}
df = df_clara


trackName = [df["song_Name"], df["song_Name"]]
artist = [df["artist"], df["artist"]]
timeStamp = df["TIME_STAMP"]
timeStamp = pd.to_datetime(timeStamp)
timeStamp = timeStamp + timedelta(hours=2)   # adding 2 hours because the time is not right
timeStamp = [timeStamp, timeStamp]

BBscore = str(df["popularity"].mean())

### AB HIER BRAUCH ICH DAS NEUE DATAFRAME
# features = ["danceability", "liveness", "energy", "instrumentalness", "speechiness", "acoustiness"]
# mean_values_spider = df[features].mean()
mean_values_spider = [[0.2,0.4,0.8, 0.5, 0.1, 0.1415], [0.1,0.5,0.7, 0.7, 0.3, 0.2415]]


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
        html.Div(id='bbScore', className='neonText', children=BBscore),
        dcc.Checklist(['Clara', 'Lukas', 'Johannes'], id = 'checklist')
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

def radarPlot(nested_list_values, names):
    subjects = ["danceability", "liveness", "energy",
                "instrumentalness", "speechiness", "acoustiness"]


    df_radar = pd.DataFrame({'subjects': [], 'values': [], 'Account' : []})
    for i in range(len(nested_list_values)):
        values = nested_list_values[i]
        df_temp = pd.DataFrame({'subjects': subjects, 'values': values, 'Account':[names[i] for k in values]})
        df_radar = pd.concat([df_radar, df_temp], axis = 0)

    fig = px.line_polar(df_radar, r='values', theta='subjects', color = 'Account',
                        line_close=True,
                        color_discrete_sequence=px.colors.sequential.Plasma_r[0:len(names)])

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
        font_color = 'white'
    )

    return fig


@callback(
    Output(component_id='spyder-graph', component_property='figure'),
    Input('checklist', 'value')
)
def update_spyder_graph(value):
    if value is None or value == []: 
        return radarPlot([[0 for i in range(6)]], ['' for i in range(6)])
    else:
        mean_values_spider = []
        names = []
        for name in value:
            df_temp = dict_df[name]
            mean_values_spider.append([np.random.uniform(0,1) for i in range(6)])
            names.append(name)
    return radarPlot(mean_values_spider,names)


# -------- Time Plot ----------------------------


def timelineTracks(nested_list_col_tracks, nested_list_col_time, nested_list_artist, names):
    df_timeline = pd.DataFrame({'col_time': [], 'col_tracks': [], 'artist': [], 'dummy': [], 'Account': []})
    for i in range(len(nested_list_artist)):
        artist = nested_list_artist[i]
        col_time = nested_list_col_time[i]
        col_tracks = nested_list_col_tracks[i]
        df_temp = pd.DataFrame({'col_time': col_time, 'col_tracks': col_tracks, 'artist': artist, 'dummy': [i for k in artist], 'Account':[names[i] for k in artist]})
        df_timeline = pd.concat([df_timeline, df_temp], axis = 0)

    fig = px.scatter(df_timeline, x='col_time', y='dummy', color = 'Account',
                     title="Time Line of the last Songs you've listened to",
                     #hover_name='col_tracks' + ' - ' + 'artist',
                     hover_data={'col_time': False, 'col_tracks': False, 'artist': False},
                     color_discrete_sequence=px.colors.sequential.Plasma_r[0:len(names)])

    fig.update_traces(marker=dict(size=15, opacity=0.6),
                      hovertemplate='<b>%{text}</b><br><br>%{x}',
                      text=df_timeline['col_tracks'] +
                      " - " + df_timeline['artist'])
    
    for i in df_timeline['dummy'].unique():
        fig.add_hline(y=i, line_color=px.colors.sequential.Plasma_r[int(i)])

    fig.update_xaxes(title_text=' ',
                     tickfont=dict(color='white'))

    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=10),
        hoverlabel=dict(
            font_size=13
        ),
        yaxis=dict(visible=False),
        title_font=dict(color='white'),
        font_color = 'white',

        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',  # this makes the background transparent
    )

    return fig


@callback(
    Output(component_id='timeline-graph', component_property='figure'),
    Input('checklist', 'value')
)
def update_timeline_graph(value):
    print(value)
    if value is None or value == []:
        return timelineTracks([], [], [], [])
    else:
        trackName = []
        timeStamp = []
        artist = []
        names = []
        for name in value:
            names.append(name)
            df_temp = dict_df[name]
            trackName.append(df_temp['song_Name'])
            artist.append(df_temp["artist"])
            timestamp_temp = df_temp["TIME_STAMP"]
            timestamp_temp = pd.to_datetime(timestamp_temp)
            timestamp_temp = timestamp_temp + timedelta(hours=2)   # adding 2 hours because the time is not right
            timeStamp.append(timestamp_temp)
        return timelineTracks(trackName, timeStamp, artist, names)


# # -------- Song Info ----------------------------

@app.callback(
    Output('song-info', 'children'),
    Input('timeline-graph', 'clickData')
)
def update_song_info(click_data):
    print(click_data)
    if click_data is not None:
        relevant = click_data['points'][0]['customdata']
        #point_index = click_data['points'][0]['pointIndex']
        track_info = str(relevant[0]) + \
            " by " + str(relevant[1])

        return html.Div([
            html.Div(id='song-box', className='neonText',
                     children='Song Information'),
            html.Div(id='selected-song', className='neonText',
                     children=track_info)
        ])
    else:
        return html.Div([
            html.Div(id='song-box', className='neonText',
                    children='Song Information'),
            html.Div(id='selected-song', className='neonText',
                    children="Please select a Song in\nthe Time Line")
    ])




if __name__ == '__main__':
    app.run_server(debug=True)
