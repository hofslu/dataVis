
"""
[Resouces]
    RangeSlider: https://community.plotly.com/t/dash-range-slider-with-date/17915/5 


TODO: Dataframe time to datetime-Object

"""

import dash
from dash import dcc, html, callback, Output, Input
import pandas as pd
import plotly.express as px


greenSpotify = 'rgb(30, 215, 96)'   # the official green spotify uses
# the official black spotify uses - for either only the user or the whole background
blackSpotify = 'rgb(25, 20, 20)'
# the other black - so its not so monotone
lightblackSpotify = 'rgb(41, 40, 40)'


app = dash.Dash(__name__, external_stylesheets=['../static/css/test.css'])

app.layout = html.Div([
    # User Info
    html.Div(id='user-info', className='neonBox', children=[
        html.Div(id='info-header', className='neonText',
                 children='Clara Fall'),
        dcc.Input(id='my-input', value='initial value',
                  type='text'),  # dummy input

        html.Div(className='neonText', children='Basic bitch score:'),
        html.Div(id='bbScore', className='neonText', children='99')
    ]),
    # Spider Chart
    html.Div(id='spider-chart', className='neonBox', children=[
        dcc.Graph(figure={}, id='spyder-graph')
    ]),
    # Time Line
    html.Div(id='timeline', className='neonBox', children=[
        dcc.Graph(figure={}, id='timeline-graph'),
        # dcc.RangeSlider(0, 100,
        #                 value=[10, 65],
        #                 tooltip={"placement": "top", "always_visible": True},
        #                 marks={
        #                     0: {'label': '0°C', 'style': {'color': '#77b0b1'}},
        #                     26: {'label': '26°C'},
        #                     37: {'label': '37°C'},
        #                     100: {'label': '100°C', 'style': {'color': '#f50'}}
        #                 },
        #                 allowCross=False,
        #                 id='python_dash_range_slider')
    ])
])


def radarPlot(dance, live, energy, instru, speech, acoust):
    subjects = ["danceability", "liveness", "energy",
                "instrumentalness", "speechiness", "acoustiness"]
    values = [dance, live, energy, instru, speech, acoust]

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
    return radarPlot(0.2, 0.6, 0.04, 0.3, 0.8, 0.9)


def timelineTracks(col_tracks, col_time):
    colTime = pd.to_datetime(col_time)
    df_timeline = pd.DataFrame({'col_time': colTime, 'col_tracks': col_tracks})

    fig = px.scatter(df_timeline, x='col_time', y=[0] * len(col_time),
                     title="Time Line of the last Songs you've listened to",
                     hover_name='col_tracks',
                     hover_data={'col_time': False, 'col_tracks': False},
                     color_discrete_sequence=[greenSpotify])

    fig.update_traces(marker=dict(size=15, opacity=0.6),
                      hovertemplate='<b>%{text}</b><br><br>%{x}',
                      text=df_timeline['col_tracks'],
                      hoverlabel=dict(bgcolor=greenSpotify))

    fig.add_hline(y=0, line_color=greenSpotify)

    fig.update_xaxes(title_text=' ')

    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=10),
        hoverlabel=dict(
            font_size=13
        ),
        yaxis=dict(visible=False),
        showlegend=False,

        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',  # this makes the background transparent
    )

    return fig


@callback(
    Output(component_id='timeline-graph', component_property='figure'),
    Input('my-input', 'value')
)
def update_timeline_graph(value):
    times = ["2023-06-12T16:06:43.007Z", "2023-06-12T16:42:41.080Z",
             "2023-06-11T16:02:41.080Z", "2023-06-11T22:02:41.080Z",
             "2023-06-12T01:02:41.080Z"]
    tracks = ["song - 12.6 um 16:06", "song - 12.6 um 16:02",
              "song - 11.6 um 16:02", "song - 11.6 um 22",
              "song - 12.6 um 01"]
    return timelineTracks(tracks, times)


if __name__ == '__main__':
    app.run_server(debug=False)
