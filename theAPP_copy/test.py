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
from dash import dash_table
from dash_table.Format import Group

from scripts.utils import get_df

# colors
greenSpotify = 'rgb(30, 215, 96)'
blackSpotify = 'rgb(25, 20, 20)'
lightblackSpotify = 'rgb(41, 40, 40)'

# name colors
name_colors = ['limegreen', 'darkturquoise', 'deeppink']


LUKAS_CLIENT_ID = "207e1c72689d4a0a88e0e721cb9bb254"
LUKAS_CLIENT_SECRET = "829b022bc7cc4559bde70a7dc57a4317"

CLARA_CLIENT_ID = "58b1a904e6d447f28c57ce10c8b8880c"
CLARA_CLIENT_SECRET = "6e2d14807777498fba48d13dd557aaeb"

JOHANNES_CLIENT_ID = 'ef739fe8683f4dada353b4260519e694'
JOHANNES_CLIENT_SECRET = '5076481d53f24b1384fc79754f35a82c'


# df = get_df(CLARA_CLIENT_ID, CLARA_CLIENT_SECRET)

try:
    df_clara = get_df(CLARA_CLIENT_ID, CLARA_CLIENT_SECRET, 'clara')
    df_lukas = get_df(LUKAS_CLIENT_ID, LUKAS_CLIENT_SECRET, 'lukas')
    df_johannes = get_df(JOHANNES_CLIENT_ID, JOHANNES_CLIENT_SECRET, 'johannes')
    df_clara.to_csv('./data/claras_songs.csv')
    df_lukas.to_csv('./data/lukas_songs.csv')
    df_johannes.to_csv('./data/johannes_songs.csv')
except:
    df_clara = pd.read_csv("/home/johannes/Dokumente/tu/info_vis/dataVis/theAPP_copy/data/claras_songs.csv")
    df_lukas = pd.read_csv("/home/johannes/Dokumente/tu/info_vis/dataVis/theAPP_copy/data/claras_songs.csv")
    df_johannes = pd.read_csv("/home/johannes/Dokumente/tu/info_vis/dataVis/theAPP_copy/data/claras_songs.csv")
    

dict_df = {'Clara': df_clara, 'Lukas': df_lukas, 'Johannes': df_johannes}


features = ["danceability", "energy", "speechiness",
            "acousticness", "instrumentalness", "liveness"]


# building the app
app = dash.Dash(__name__, external_stylesheets=['../static/css/test2.css'])

app.layout = html.Div([
    # User Info
    html.Div(id='user-info', className='neonBox', children=[
        html.Div(id='user', className='neonText',
                 children='Spotify User Data'),
        # User selection
        dcc.Checklist(
            ['Clara', 'Lukas', 'Johannes'],

            value=['Clara'],
            id='checklist',
            inputClassName='checkboxDash'
        ),
        # User scores
        html.Div(id='table-scores', className=''
                 ),
    ]),
    # Spider Chart
    html.Div(id='spider-chart', className='neonBox', children=[
        dcc.Graph(figure={}, id='spyder-graph')

    ]),
    # Song Info
    html.Div(id='song-info', className='neonBox', children = [
        dcc.Graph(figure = {}, id = 'song-graph')
    ]),

    # Time Line
    html.Div(id='timeline', className='neonBox', children=[
        html.Div(id='title_timeline', className='neonText',
                 children='Time Line of the last 50 recently played Songs'),
        dcc.Graph(figure={}, id='timeline-graph')
    ])
])


# -------- Radar(Spider) Plot ----------------------------

def radarPlot(df_radar_input):
    subjects = features
    df_radarplot = pd.DataFrame({'subjects': [], 'values': [], 'Account': []})

    for i in range(len(df_radar_input)):
        values = df_radar_input.loc[i, subjects]
        df_temp = pd.DataFrame({'subjects': subjects, 'values': values, 'Account': [
                               df_radar_input.loc[i, "name"] for _ in values]})
        df_radarplot = pd.concat([df_radarplot, df_temp], ignore_index=True)

    name_colors_radar = name_colors[:len(df_radar_input["name"])]
    if len(df_radar_input) == 0:
        df_radarplot = pd.DataFrame({'subjects': features, 'values': [0,0,0,0,0,0], 'Account': np.full(6, "None")})
        name_colors_radar = ["rgba(0,0,0,0)"]

    fig = px.line_polar(df_radarplot, r='values', theta='subjects', color='Account',
                        line_close=True, # THIS BITCH GAVE ME AN ERROR I WAS LOOKING EVERYWHERE FOR
                        color_discrete_sequence=name_colors_radar
                        )

    fig.update_traces(fill="toself")

    fig.update_polars(bgcolor=blackSpotify)

    fig.update_layout(
        autosize=True,
        height=None,
        width=None,
        polar=dict(
            radialaxis=dict(
                tickfont=dict(color='white'),
                range=[0, 1],
                tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1],
            ),
            angularaxis=dict(
                tickfont=dict(color='white')
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',  # this makes the background transparent
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )

    return fig


@callback(
    Output(component_id='spyder-graph', component_property='figure'),
    Input('checklist', 'value')
)
def update_spyder_graph(checked):
    cols = features+["name"]
    if checked is None or checked == []:
        df_radar=pd.DataFrame([], columns=cols)

    else:
        df_radar = pd.DataFrame(data=[], columns=features + ["name"])
        for name in checked:
            tmp_row = dict_df[name][features].mean().values.tolist() + [name]
            tmp_df = pd.DataFrame([tmp_row], columns=cols)
            df_radar = pd.concat([df_radar, tmp_df], ignore_index=True)

    return radarPlot(df_radar)


# -------- Time Plot ----------------------------

def timelineTracks(nested_list_col_tracks, nested_list_col_time, nested_list_artist, names):
    df_timeline = pd.DataFrame(
        {'col_time': [], 'col_tracks': [], 'artist': [], 'dummy': [], 'Account': []})
    for i in range(len(nested_list_artist)):
        artist = nested_list_artist[i]
        col_time = nested_list_col_time[i]
        col_tracks = nested_list_col_tracks[i]
        df_temp = pd.DataFrame({'col_time': col_time, 'col_tracks': col_tracks, 'artist': artist, 'dummy': [
                               i for k in artist], 'Account': [names[i] for k in artist]})
        df_timeline = pd.concat([df_timeline, df_temp], axis=0)

    fig = px.scatter(df_timeline, x='col_time', y='dummy', color='Account',
                     # title="Time Line of the last Songs you've listened to",
                     # hover_name='col_tracks' + ' - ' + 'artist',
                     hover_data={'col_time': False,
                                 'col_tracks': False, 'artist': False, 'dummy': False},
                     color_discrete_sequence=name_colors[0:len(names)])
    
    if nested_list_col_tracks != []:
        fig.update_traces(marker=dict(size=15, opacity=0.6),
                        hovertemplate='<b>%{text}</b><br><br>%{x}',
                        text=df_timeline['col_tracks'] +
                        " - " + df_timeline['artist']
                        # + " - " + df_timeline['artist']
                        )

    for i in df_timeline['dummy'].unique():
        fig.add_hline(y=i, line_color=name_colors[int(i)])

    fig.update_xaxes(title_text=' ',
                     tickfont=dict(color='white'))

    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=10),
        hoverlabel=dict(
            font_size=13
        ),
        yaxis=dict(visible=False),
        title_font=dict(color='white'),
        font_color='white',

        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',  # this makes the background transparent
    )

    return fig


@callback(
    Output(component_id='timeline-graph', component_property='figure'),
    Input('checklist', 'value')
)
def update_timeline_graph(checked):
    print(checked)
    if checked is None or checked == []:
        return timelineTracks([], [], [], [])
    else:
        trackName = []
        timeStamp = []
        artist = []
        names = []
        for name in checked:
            names.append(name)
            df_temp = dict_df[name]
            trackName.append(df_temp['song_Name'])
            artist.append(df_temp["artist"])
            timestamp_temp = df_temp["TIME_STAMP"]
            timestamp_temp = pd.to_datetime(timestamp_temp)
            # adding 2 hours because the time is not right
            timestamp_temp = timestamp_temp + timedelta(hours=2)
            timeStamp.append(timestamp_temp)
        
        return timelineTracks(trackName, timeStamp, artist, names)


# # -------- Song Info ----------------------------

def radarPlot2(input):
    data = pd.DataFrame({'subjects' : features,
                          'values': input})
    fig = px.line_polar(data, r='values', theta='subjects',
                        line_close=True, # THIS BITCH GAVE ME AN ERROR I WAS LOOKING EVERYWHERE FOR
                        color_discrete_sequence=[name_colors[0]]
                        )
    fig.update_traces(fill="toself")

    fig.update_polars(bgcolor=blackSpotify)

    fig.update_layout(
        autosize=True,
        height=None,
        width=None,
        polar=dict(
            radialaxis=dict(
                tickfont=dict(color='white'),
                range=[0, 1],
                tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1],
            ),
            angularaxis=dict(
                tickfont=dict(color='white')
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',  # this makes the background transparent
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )

    return fig

@app.callback(
    Output('song-info', 'children'),
    Input('timeline-graph', 'clickData')
)
def update_song_info(click_data):
    print(click_data)
    if click_data is not None:
        relevant = click_data['points'][0]['text']
        #print(relevant)
        # point_index = click_data['points'][0]['pointIndex']
        track_info = relevant
        song, artist = click_data['points'][0]['customdata']
        for name in dict_df.keys():
            df = dict_df[name]
            tmp = df.loc[(df['artist'] == artist) & (df['song_Name'] == song), features]
            if len(tmp) > 0:
                break
        data = tmp.iloc[0].to_list()
        fig = radarPlot2(data)

        return html.Div([
            html.Div(id='song-box', className='neonText',
                     children='Song Information'),
            html.Div(id='selected-song', className='neonText',
                     children=track_info),
            dcc.Graph(figure = fig, id = 'song-graph')
        ])
    else:
        return html.Div([
            html.Div(id='song-box', className='neonText',
                     children='Song Information'),
            html.Div(id='selected-song', className='neonText',
                     children="Please select a Song in\nthe Time Line")
        ])
    
#--------- song bar plor ---------------------------

# -------- table scores ----------------------------

@callback(
    Output(component_id='table-scores', component_property='children'),
    Input('checklist', 'value')
)
def update_user_scores(checked):
    #print(checked)
    df_tmp = pd.DataFrame({'features': features})
    bbscores = []

    for name in checked:
        df_tmp_full = dict_df[name]
        pop_tmp = np.round(df_tmp_full['popularity'].mean(), 2)
        bbscores = bbscores + [pop_tmp]
        feat_tmp = np.round(df_tmp_full[features].mean().values, 2)
        df_tmp[name] = feat_tmp

    strBB = ""
    for score in bbscores[:-1]:
        strBB = strBB + str(score) + ", "
    if bbscores != []:
        strBB += str(bbscores[-1])
    else:
        pass

    return [
        html.Div(id='bbScore', className='neonText',
                 children="BB score: \n" + strBB),
        dash_table.DataTable(
            id='feature-table',
            columns=[{'name': col, 'id': col} for col in df_tmp.columns],
            data=df_tmp.to_dict('records'),
            style_table={'width': '100%'},
            style_cell={
                'textAlign': 'left',
                'backgroundColor': 'rgba(0,0,0,0)',
                'color': 'white',
                'padding': '6px',
                'fontSize': '12px'
            },
            style_header={
                'backgroundColor': 'rgba(0,0,0,0)',
                'fontWeight': 'bold',
                'color': 'white',
                'padding': '6px',
                'fontSize': '12px'
            }
        )
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
