# Import required libraries
import pandas as pd
import numpy as np
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

# Clear the layout and do not display exception till callback gets executed
# app.config.suppress_callback_exceptions = True

# Read the wildfire data into pandas dataframe
df =  pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
df.drop("Unnamed: 0",axis=1,inplace=True)
# create launchsite dropdown options 
launch_site_list = ['All']
launch_site_list = np.append(launch_site_list,df['Launch Site'].unique())
   
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(launch_site_list,
                                             value='All',
                                             placeholder='Select a Launch Site',
                                             searchable=True,
                                             id='site-dropdown'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min=0, max=10000, step=1000,value=[2500, 8000],id='payload-slider',),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'All':        
        fig = px.pie(df,values='class',names='Launch Site',title='Total Success of {} Luanches by Site'.format(entered_site))
        return fig
    else:
        filtered_df = df[df['Launch Site']==entered_site]
        fig = px.pie(filtered_df,values='class',names='class',title='Total Success of {} Luanches by Site'.format(entered_site))
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),            [Input(component_id='site-dropdown', component_property='value'),Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site,slider_range):
    low, high = slider_range
    
    if entered_site == 'All':     
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)           
        fig = px.scatter(df[mask], y="class", x="Payload Mass (kg)", color="Booster Version Category")
        return fig
    else:
        filtered_df = df[df['Launch Site']==entered_site]
        mask = (filtered_df['Payload Mass (kg)'] > low) & (filtered_df['Payload Mass (kg)'] < high)
        fig = px.scatter(filtered_df[mask], y="class", x="Payload Mass (kg)", color="Booster Version Category")
        return fig
    
    
# Run the app
if __name__ == '__main__':
    app.run_server()
