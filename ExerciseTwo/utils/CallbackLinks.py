from dash import callback, Output, Input
import plotly.express as px

# Add controls to build the interaction
@callback(
    Output(component_id='map-graph', component_property='figure'),
    Input(component_id='drop-down-world-representation-item', component_property='value')
)
def update_map(style):
    return build_world_map(style)


# Add controls to build the interaction
@callback(
    Output(component_id='scatter-graph', component_property='figure'),
    Input(component_id='drop-down-country-attribute-item', component_property='value')
)
def update_scatter(col_chosen):
    df_PCA = PrComAnalysis(df, col_chosen)          ####    clara aenderung
    fig = px.scatter(df_PCA, x=df_PCA['PC1'], y=df_PCA['PC2'], 
                     title = "PCA -" + col_chosen,
                     hover_name='Country Code',
                     hover_data = {'PC1': False, 'PC2':False})      #### clara aenderung

    fig.update_traces(marker=dict(size= 15, color='lightpink', opacity=0.6))

    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=10),
        hoverlabel=dict(
        font_size=13
        )  
    )
    return fig


# Add controls to build the interaction
@callback(
    Output(component_id='time-line-graph', component_property='figure'),
    Input(component_id='scatter-graph', component_property='clickData'),
    # Input(component_id='drop-down-country-code-item', component_property='value'),
    Input(component_id='drop-down-country-attribute-item', component_property='value')
)
def update_time_line(country_chosen, attr_chosen):
    country_chosen = country_chosen['points'][0]['hovertext']
    indices = df.index[df['Country Code'] == country_chosen].tolist()
    start = min(indices)
    end = max(indices)
    # x, y = from_function(df)
    fig = px.line(df, x=df['year'][start:end], y=df[attr_chosen].iloc[start:end], 
                  title=country_chosen + " - " + attr_chosen, 
                  labels={
                     'x': "Year",
                     'y': attr_chosen})         #### clara aenderung
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
    fig.update_traces(line_color='lightpink')           #### clara aenderung
    return fig


@callback(
    Output(component_id='debug-line', component_property='children'),
    Input(component_id='scatter-graph', component_property='clickData')
)
def update_debug_line(data):
    print(data)
