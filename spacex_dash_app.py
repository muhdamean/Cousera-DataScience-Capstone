# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
launch_site = spacex_df.groupby('Launch Site')
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',
                                #                 options=[
                                #                 {"label": name, "value": name} for name in launch_site['Launch Site']
                                #                 ],
                                #                 value="ALL Sites",
                                #                 clearable=False,
                                #             ),
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                             ],
                                             value='ALL Sites',
                                             placeholder='Select a Launch Site here',
                                             searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=100,
                                                value=[spacex_df['Payload Mass (kg)'].min(),
                                                       spacex_df['Payload Mass (kg)'].max()]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_graph(entered_site):
    # Select data for custom Launch Site
    if entered_site == 'ALL':
        df = spacex_df[spacex_df['class'] == 1]  # making new df where only records with successfull starts are taken
        new_df = df[['class', 'Launch Site']]
        pie_data = new_df.groupby(['Launch Site'], as_index=False).count()
        fig = px.pie(pie_data, values=pie_data['class'], names=pie_data['Launch Site'],
                     title='Successfull Launches Distributed by Launch Sites')
    else:
        df = spacex_df[spacex_df['Launch Site'] == entered_site]
        new_df = df[['class', 'Flight Number']]
        pie_data = new_df.groupby(['class'], as_index=False).count()
        fig = px.pie(pie_data, values=pie_data['Flight Number'], names=pie_data['class'],
                     title='Success (1)/Failure (0) Launches for Site ' + format(entered_site))
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_graph_slider(entered_site, slider_range):
    low, high = slider_range
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    new_spacex_df = spacex_df[mask]

    if entered_site == 'ALL Sites':
        df = new_spacex_df
        fig = px.scatter(df, x=df['Payload Mass (kg)'], y=df['class'], color=df['Booster Version Category'])
    else:
        df = new_spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.scatter(df, x=df['Payload Mass (kg)'], y=df['class'], color=df['Booster Version Category'])
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
