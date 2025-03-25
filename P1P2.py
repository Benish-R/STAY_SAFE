import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Initialize the Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Global variable to store travel information
travel_data = {}

# Main layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # This is needed for routing
    html.Div(id='page-content')  # This will hold the content of the current page
])

# Layout for the first page
def first_page():
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Travel Information Form", className="text-center"), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dbc.Input(id='name', placeholder='Enter your name', type='text'), width=12)
        ], className="mb-2"),
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='level',
                options=[{'label': str(i), 'value': str(i)} for i in range(50, 55)],
                placeholder='Select your level',
            ), width=12)
        ], className="mb-2"),
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='location',
                options=[
                    {'label': 'Coimbatore', 'value': 'Coimbatore'},
                    {'label': 'Bangalore', 'value': 'Bangalore'},
                    {'label': 'Hyderabad', 'value': 'Hyderabad'}
                ],
                placeholder='Select your location',
            ), width=12)
        ], className="mb-2"),
        dbc.Row([
            dbc.Col(dcc.DatePickerSingle(
                id='date',
                placeholder='Select a date',
            ), width=12)
        ], className="mb-2"),
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='meal',
                options=[
                    {'label': 'Veg', 'value': 'Veg'},
                    {'label': 'Non-Veg', 'value': 'Non-Veg'}
                ],
                placeholder='Select meal preference',
            ), width=12)
        ], className="mb-2"),
        dbc.Row([
            dbc.Col(dbc.Input(id='members', placeholder='Travelling with members', type='text'), width=12)
        ], className="mb-2"),
        dbc.Row([
            dbc.Col(dbc.Input(id='purpose', placeholder='Purpose of travel', type='text'), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dbc.Button('Submit', id='submit-button', color='primary', className="btn-block"), width=12)
        ]),
        dbc.Row([
            dbc.Col(html.Div(id='output-message', className="mt-4"), width=12)
        ])
    ], fluid=True)

# Layout for the second page
def second_page(travel_info):
    display_data = [html.Li(f"{key}: {value}") for key, value in travel_info.items()]
    return dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Submitted Travel Information", className="text-center"), width=12)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(html.Ul(display_data), width=12)
        ])
    ], fluid=True)

# Callback to handle the submission and navigation
@app.callback(
    [Output('url', 'pathname'),
     Output('output-message', 'children')],
    [Input('submit-button', 'n_clicks')],
    [State('name', 'value'),
     State('level', 'value'),
     State('purpose', 'value'),
     State('location', 'value'),
     State('date', 'date'),
     State('meal', 'value'),
     State('members', 'value')]
)
def update_output(n_clicks, name, level, purpose, location, date, meal, members):
    if n_clicks is None:
        return dash.no_update, ""
    
    # Create a travel information dictionary
    travel_info = {
        "Name": name,
        "Level": level,
        "Purpose": purpose,
        "Location": location,
        "Date": date,
        "Meal Preference": meal,
        "Travelling With Members": members
    }

    # Store info in the global variable
    travel_data.update(travel_info)

    # Navigate to the second page
    return '/submitted', "Your information has been submitted!"

# Callback to display the relevant page based on URL
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/submitted':
        return second_page(travel_data)
    return first_page()  # Default to the first page

# Run the app
if __name__ == '__main__':
    app.run(debug=True)  # Use app.run(debug=True) only for development