from dash import Input, Output
from layouts.entity_layout import create_entity_layout
from layouts.cluster_layout import create_cluster_layout


def register_tabs_callbacks(app, df, min_year, max_year):
    """
    Registers callback functions for handling tab navigation and rendering
    different content layouts based on the selected tab.
    """

    @app.callback(
        Output("tabs-content-page-1", "children"),
        Input("page-1-tabs", "value"),
    )
    def render_page_1_tabs(tab):
        """
        Callback function to render content based on the selected tab.
        Renders the corresponding layout (cluster or entity)
        by passing relevant data like the DataFrame and awarded year range.
        """
        if tab == "cluster-tab":
            # Collect summary statistics for descriptive analysis
            summary_data = dict()
            summary_data["total_entities"] = df[
                "ENTITY"
            ].nunique()  # Count of unique entities
            summary_data["total_vendors"] = df[
                "VENDOR"
            ].nunique()  # Count of unique vendors
            summary_data["min_awarded_amount"] = df[
                "AWARDED_AMOUNT"
            ].min()  # Minimum awarded amount
            summary_data["max_awarded_amount"] = df[
                "AWARDED_AMOUNT"
            ].max()  # Maximum awarded amount
            summary_data["min_awarded_year"] = min_year  # Minimum awarded year
            summary_data["max_awarded_year"] = max_year  # Maximum awarded year
            return create_cluster_layout(
                df, min_year, max_year, summary_data
            )  # Render cluster analysis layout

        elif tab == "entity-tab":
            return create_entity_layout(
                df, min_year, max_year
            )  # Render entity-based analysis layout
