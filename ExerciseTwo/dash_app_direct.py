
from dash import Dash, html, dash_table, dcc, callback, Output, Input

import dash_bootstrap_components as dbc
import plotly.express as px

import pandas as pd

import os

selection = ['Country Name', 'Country Code', 'year', 'Agricultural land (% of land area)', 'Agricultural land (sq. km)', 'Arable land (% of land area)', 'Arable land (hectares per person)', 'Arable land (hectares)', 'Birth rate, crude (per 1,000 people)', 'Death rate, crude (per 1,000 people)', 'GDP per capita (current US$)', 'Land area (sq. km)', 'Population, total', 'Rural population', 'Rural population (% of total population)', 'Rural population growth (annual %)', 'Surface area (sq. km)']


def build_map_from_df(df):
    fig = 'Choropleth-Map'
    return fig

def build_tooltip(df, selection):
    tooltip = {
        "attributeOne": 1,
        "attributeTwo": 2,
        "attributeString": "Information",
    }
    return tooltip

def build_PCA(df, attribute):
    """builds PCA scatter-data-frame for each country, based on attribute-selection

    Args:
        df (Pandas.DataFrame): the actual data frame
        attribute (string): the attribute selection string

    Returns:
        Pandas.DataFrame: head{adCountryCode, PCA1, PCA2}
    """

def build_time_line(df, selection):
    """builds dataframe for time-series representation

    Args:
        df (Pandas.DataFrame): full data-frame
        selection (string): Country Code

    Returns:
        Pandas.DataFrame: head(Year, selection)
    """
    return 



# -----------------------------------------------------------------------------------
from sklearn.decomposition import PCA
from sklearn import preprocessing

def PrComAnalysis(df, string):
    df_2020 = df[df["year"] == 2020].copy()

    # distributing the dataset into two components X and Y
    tmp = list(df_2020.columns)
    tmp.remove(string)
    tmp.remove('Country Name')
    tmp.remove('Country Code')
    tmp.remove('year') 

    # distributing the dataset into two components X and y
    # We decided to do the regression on Agricultural land (% of land area)
    X = df_2020[tmp].values 
    y =  df_2020.loc[:,[string]].values

    # fitting the Standard scale
    X_scaled = preprocessing.scale(X)

    # Create a PCA object and fit it to the data
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(X_scaled)

    df_PCA = pd.DataFrame(data = principalComponents, index = df_2020['Country Code'].values
                          , columns = ['PC1', 'PC2'])
    
    return df_PCA
# -----------------------------------------------------------------------------------

# load data
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = pd.read_csv('./data/preproc_claras_dataframe.csv')


# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)


# App layout
app.layout = dbc.Container([
    # dbc.Row([
    #     html.H1("This is our first python dash(board) app :)")
    # ]),

    dbc.Row([
        dbc.Col([
                dbc.Row([
                    dcc.Dropdown(list(set(df['Country Code'])), 'AUT', id='drop-down-country-code-item'),
                    dcc.Dropdown(selection, 'Country Code', id='drop-down-country-attribute-item'),
                ]),
                dbc.Row([
                    # World-map
                    dcc.Graph(
                        figure={}, id='map-graph',
                        style={
                            'height': '325px',
                            }
                    )
                ]),
        ]),
        dbc.Col(
            # Scatter-Plot
            dcc.Graph(figure={}, id='scatter-graph',
                style={
                    # "background-color": "#ADD8E6",
                    'height': '350px',
                    'width': 'auto'
                }),
                width=6, 
            ),
    ], style={
        "height": "350px",
        "overflow": "hidden"
        }),
    dbc.Row([
        dbc.Col(
            # Time-Line
            dcc.Graph(figure={}, id='time-line-graph',
            style={
                'height': '375px',
                'width': 'auto'
            }),
            width=6, style={
                # "background-color": "#D8BFD8",
                }
            ),
        dbc.Col(
            # detailed-information
            dash_table.DataTable(data=df.to_dict('records'), 
            page_size=10
            ),
            width=6,
            ),
    ], style={
        "height": "350px",
        # "overflow": "hidden"
        })

],style={
    "height": "100vh", 
    "width": "100vw", 
    # "background-color": "wheat",
    "overflow": "hidden",
    })



# Add controls to build the interaction
@callback(
    Output(component_id='map-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    fig.update_layout(margin=dict(l=0, r=0, t=5, b=0))
    return fig


# Add controls to build the interaction
@callback(
    Output(component_id='scatter-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.scatter(df, x='continent', y='continent')
    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=10),
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 0.5,
            dtick = 0.75
        ),
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0.5,
            dtick = 0.75
        )
        )
    return fig


# Add controls to build the interaction
@callback(
    Output(component_id='time-line-graph', component_property='figure'),
    Input(component_id='drop-down-country-code-item', component_property='value'),
    Input(component_id='drop-down-country-attribute-item', component_property='value')
)

def update_graph(country_chosen, attr_chosen):
    indices = df.index[df['Country Code'] == country_chosen].tolist()
    start = min(indices)
    end = max(indices)
    fig = px.line(df, x=df['year'][start:end], y=df[attr_chosen].iloc[start:end], title=country_chosen + " - " + attr_chosen)
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
    return fig



# ------------------ VIEWs ------------------ 
#   Map: 
#   ScatterPlot:
#   TimeSeries: add Time-Selection
#   DataFrame: 


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
