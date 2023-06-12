import dash
from dash import dcc, html

app = dash.Dash(__name__, external_stylesheets=['../static/css/test.css'])

app.layout = html.Div([
    # User Info
    html.Div(id='user-info', className='neonBox', children=[
        html.Div(id='info-header', className='neonText',
                 children='Clara Fall'),
        html.Div(className='neonText', children='Basic bitch score:'),
        html.Div(id='bbScore', className='neonText', children='99')
    ]),
    # Spider Chart
    html.Div(id='spider-chart', className='neonBox'),
    # Time Line
    html.Div(id='timeline', className='neonBox', children=[
        dcc.RangeSlider(0, 100,
                        value=[10, 65],
                        tooltip={"placement": "top", "always_visible": True},
                        marks={
                            0: {'label': '0°C', 'style': {'color': '#77b0b1'}},
                            26: {'label': '26°C'},
                            37: {'label': '37°C'},
                            100: {'label': '100°C', 'style': {'color': '#f50'}}
                        },
                        allowCross=False,
                        id='python_dash_range_slider')
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
