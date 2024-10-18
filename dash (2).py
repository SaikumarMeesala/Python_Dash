import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import json
import pandas as pd
import os

# Load the JSON data
def load_data():
    with open(os.path.join('data', 'data.json')) as f:
        return json.load(f)
data = load_data()

# Convert JSON data to a pandas DataFrame
df = pd.DataFrame(data)

# Create the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1('Population Review Dashboard'),

    # Dropdown for selecting the state
    html.Label('Select State:'),
    dcc.Dropdown(
        id='state-dropdown',
        options=[{'label': state, 'value': state} for state in df['State'].unique()],
        value='Alabama' , # Default value
        placeholder="State state name",
        clearable=True
    ),

    # Dropdown for selecting the year
    html.Label('Select Year:'),
    dcc.Dropdown(
        id='year-dropdown',
        options=[],
        value=None  # This will be updated dynamically
    
    ),

    # Graphs
    dcc.Graph(id='gender-bar-chart'),
    dcc.Graph(id='ethnicity-males-chart'),
    dcc.Graph(id='ethnicity-females-chart'),
    dcc.Graph(id='ethnicity-other-chart'),
    dcc.Graph(id='migration-bar-chart')
])

# Callback to update the year dropdown based on selected state
@app.callback(
    Output('year-dropdown', 'options'),
    Output('year-dropdown', 'value'),
    Input('state-dropdown', 'value')
)
def update_year_options(selected_state):
    filtered_df = df[df['State'] == selected_state]
    years = filtered_df['Year'].unique()
    options = [{'label': year, 'value': year} for year in years]
    return options, years[0]  # Set the first year as default

# Callback to update the graphs based on selected state and year
@app.callback(
    Output('gender-bar-chart', 'figure'),
    Output('ethnicity-males-chart', 'figure'),
    Output('ethnicity-females-chart', 'figure'),
    Output('ethnicity-other-chart', 'figure'),
    Output('migration-bar-chart', 'figure'),
    Input('state-dropdown', 'value'),
    Input('year-dropdown', 'value')
)
def update_graphs(selected_state, selected_year):
    # Filter data by state and year
    filtered_df = df[(df['State'] == selected_state) & (df['Year'] == selected_year)]
    
    # Gender Distribution Bar Chart
    gender_data = {
        'Category': ['Boys', 'Girls', 'Other'],
        'Count': [filtered_df['Boys'].values[0], filtered_df['Girls'].values[0], filtered_df['Other'].values[0]]
    }
    df_gender = pd.DataFrame(gender_data)
    gender_fig = px.bar(df_gender, x='Category', y='Count',
                        title=f'Gender Distribution in {selected_state} ({selected_year})',
                        labels={'Count': 'Population'},
                        color='Category')
    
    # Ethnicity Distribution for Males
    ethnicity_males_data = {
        'Ethnicity': ['White', 'Black', 'Asian', 'Indian', 'OtherEthnicity'],
        'Count': [filtered_df['White'].values[0] * (filtered_df['Boys'].values[0] / filtered_df['Population'].values[0]),
                  filtered_df['Black'].values[0] * (filtered_df['Boys'].values[0] / filtered_df['Population'].values[0]),
                  filtered_df['Asian'].values[0] * (filtered_df['Boys'].values[0] / filtered_df['Population'].values[0]),
                  filtered_df['Indian'].values[0] * (filtered_df['Boys'].values[0] / filtered_df['Population'].values[0]),
                  filtered_df['OtherEthnicity'].values[0] * (filtered_df['Boys'].values[0] / filtered_df['Population'].values[0])]
    }
    df_ethnicity_males = pd.DataFrame(ethnicity_males_data)
    ethnicity_males_fig = px.pie(df_ethnicity_males, values='Count', names='Ethnicity',
                                 title=f'Ethnicity Distribution of Males in {selected_state} ({selected_year})')

    
    ethnicity_females_data = {
        'Ethnicity': ['White', 'Black', 'Asian', 'Indian', 'OtherEthnicity'],
        'Count': [filtered_df['White'].values[0] * (filtered_df['Girls'].values[0] / filtered_df['Population'].values[0]),
                  filtered_df['Black'].values[0] * (filtered_df['Girls'].values[0] / filtered_df['Population'].values[0]),
                  filtered_df['Asian'].values[0] * (filtered_df['Girls'].values[0] / filtered_df['Population'].values[0]),
                  filtered_df['Indian'].values[0] * (filtered_df['Girls'].values[0] / filtered_df['Population'].values[0]),
                  filtered_df['OtherEthnicity'].values[0] * (filtered_df['Girls'].values[0] / filtered_df['Population'].values[0])]
    }
    df_ethnicity_females = pd.DataFrame(ethnicity_females_data)
    ethnicity_females_fig = px.pie(df_ethnicity_females, values='Count', names='Ethnicity',
                                   title=f'Ethnicity Distribution of Females in {selected_state} ({selected_year})')

    
    ethnicity_other_data = {
        'Ethnicity': ['White', 'Black', 'Asian', 'Indian', 'OtherEthnicity'],
        'Count': [filtered_df['White'].values[0] * (filtered_df['Other'].values[0] / filtered_df['Population'].values[0]),
                  filtered_df['Black'].values[0] * (filtered_df['Other'].values[0] / filtered_df['Population'].values[0]),
                  filtered_df['Asian'].values[0] * (filtered_df['Other'].values[0] / filtered_df['Population'].values[0]),
                  filtered_df['Indian'].values[0] * (filtered_df['Other'].values[0] / filtered_df['Population'].values[0]),
                  filtered_df['OtherEthnicity'].values[0] * (filtered_df['Other'].values[0] / filtered_df['Population'].values[0])]
    }
    df_ethnicity_other = pd.DataFrame(ethnicity_other_data)
    ethnicity_other_fig = px.pie(df_ethnicity_other, values='Count', names='Ethnicity',
                                 title=f'Ethnicity Distribution of Other Genders in {selected_state} ({selected_year})')

    
    migration_data = {
        'Status': ['Migrated', 'NonMigrated'],
        'Count': [filtered_df['Migrated'].values[0], filtered_df['NonMigrated'].values[0]]
    }
    df_migration = pd.DataFrame(migration_data)
    migration_fig = px.area(df_migration, x='Status', y='Count',
                            title=f'Migration Status in {selected_state} ({selected_year})',
                            labels={'Count': 'Population'},
                            color='Status')

    return gender_fig, ethnicity_males_fig, ethnicity_females_fig, ethnicity_other_fig, migration_fig


if __name__ == '__main__':
    app.run_server(debug=True)
