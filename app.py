import os
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from bertopic import BERTopic

# Importing callback functions
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
The Dash app is initialized with:
- suppress_callback_exceptions=True: Allows dynamic callback registration.
- Bootstrap for styling using external_stylesheets from dash_bootstrap_components.
"""
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
app.title = "Public Tender Analysis Dashboard - Nova Scotia"

# Define app layout with routing and tabs
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content"),
])

# Initialize BERTopic model (lazy-loading might be considered for performance optimization)
topic_model = BERTopic()

# Register callbacks
register_page_routing_callbacks(app)  # Callbacks for page routing are registered here
register_tabs_callbacks(app, df, min_year, max_year)  # Callbacks for tabs are registered here
register_callbacks_for_cluster(app, df, topic_model) # Callbacks for clustering are registered here
register_callbacks_for_entity(app, df, topic_model) # Callbacks for entity analysis are registered here

# Run app in debug mode (toggle for production using an environment variable)
if __name__ == "__main__":
    debug_mode = os.getenv("DEBUG", "True").lower() == "true"
    app.run_server(host="0.0.0.0", port=8050, debug=debug_mode)
