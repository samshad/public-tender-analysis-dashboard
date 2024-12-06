from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from bertopic import BERTopic

# Importing callback functions for different app features
from callbacks.callbacks_cluster import register_callbacks_for_cluster
from callbacks.callbacks_entity import register_callbacks_for_entity
from callbacks.tabs_callbacks import register_tabs_callbacks
from callbacks.routing_callbacks import register_page_routing_callbacks

# Importing data processing functions
from data_cleaning.data_loader import get_data

# Load data and prepare data
df, min_year, max_year = get_data()

# Initialize Dash app
"""
Dash app is initialized with the suppress_callback_exceptions flag set to True 
to allow dynamic callbacks (callbacks that are registered at runtime). 
The app uses Bootstrap for styling via `dash_bootstrap_components`.
"""
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Public Tender Data Analysis"

# Define app layout with routing and tabs
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content"),
])

topic_model = BERTopic()

# Register page routing callback
register_page_routing_callbacks(app)

register_tabs_callbacks(app, df, min_year, max_year)  # Callbacks for specific tabs and analysis features are registered here
register_callbacks_for_cluster(app, df, topic_model)
register_callbacks_for_entity(app, df, topic_model)

# Start the app server in debug mode for development
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
