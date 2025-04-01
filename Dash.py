# Import packages
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
# Read the dataset
df = pd.read_csv("fifa_world_cup_finals.csv")

# Initialize Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "FIFA World Cup Dashboard"

# Count wins per country
win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']

# Create the Choropleth figure
fig = px.choropleth(
    win_counts,
    locations="Country",
    locationmode="country names",
    color="Wins",
    color_continuous_scale="pinkyl",
    title="<u>FIFA World Cup Wins by Country</u>",
    projection='natural earth'
)

# Make the title look better
fig.update_layout(
    title={
        'x': 0.5,  # Center the title
        'xanchor': 'center',
        'yanchor': 'top'
    },
    title_font=dict(
        size=22,
        color='#333',
        family='Arial'
    )
)

# Get list of unique winning countries
country_options = [{'label': country, 'value': country} for country in df['Winner'].unique()]

# Get list of World Cup years
year_options = [{'label': str(y), 'value': y} for y in sorted(df['Year'].unique())]

# Dash layout
app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={
        'textAlign': 'center',
        'color': '#111111',
        'paddingTop': '20px'
    }),

    html.Div([
        dcc.Graph(figure=fig),
        
        html.Div([
            html.Label("Select a Country:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='country-dropdown',
                options=country_options,
                value='Brazil'
            ),
            html.Div(id='win-output', style={
                'marginTop': '10px',
                'fontSize': '18px',
                'color': '#333333'
            }),

            html.Br(),

            html.Label("Select a Year:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='year-dropdown',
                options=year_options,
                value=2022
            ),
            html.Div(id='match-output', style={
                'marginTop': '10px',
                'fontSize': '18px',
                'color': '#333333'
            })
        ], style={
            'width': '60%',
            'margin': 'auto',
            'padding': '20px',
            'backgroundColor': '#f9f9f9',
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        })
    ])
])

# Callback to update the text based on selected country
@app.callback(
    Output('win-output', 'children'),
    Input('country-dropdown', 'value')
)
def update_win_text(selected_country):
    win_count = df['Winner'].value_counts().get(selected_country, 0)
    return f"{selected_country} has won the World Cup {win_count} times."

@app.callback(
    Output('match-output', 'children'),
    Input('year-dropdown', 'value')
)
def update_match_result(selected_year):
    row = df[df['Year'] == selected_year]
    if not row.empty:
        winner = row.iloc[0]['Winner']
        runner_up = row.iloc[0]['Runner_Up']
        return f"In {selected_year}, {winner} won the World Cup and {runner_up} was the runner-up."
    else:
        return "No data for that year."

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
