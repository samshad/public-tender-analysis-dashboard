from dash import Input, Output, html, dcc


def register_page_routing_callbacks(app):
    """
    Registers callback functions for page routing, setting up tab navigation and rendering
    the corresponding content based on the selected tab.
    """

    # Define the default style for tabs
    tab_style = {
        "padding": "16px 20px",  # Increased padding for better spacing and size
        "borderRadius": "5px",
        "backgroundColor": "#f8f9fa",
        "border": "1px solid #dee2e6",
        "marginRight": "4px",
        "color": "#6c757d",
        "fontSize": "14px",
        "cursor": "pointer",
        "transition": "all 0.3s ease",
        "textAlign": "center",  # Center-aligns text in the tab
        "display": "flex",  # Enables flexbox for alignment
        "alignItems": "center",  # Centers content vertically
        "justifyContent": "center",  # Centers content horizontally
        "width": "150px",  # Sets consistent tab width
        "height": "40px",  # Sets consistent tab height
    }

    # Define the style for the selected tab
    tab_selected_style = {
        "padding": "16px 20px",  # Consistent padding
        "borderRadius": "5px",
        "backgroundColor": "#007bff",  # Active tab background color
        "border": "1px solid #0056b3",  # Border color for active tab
        "marginRight": "4px",
        "color": "white",  # Active tab text color
        "fontSize": "14px",
        "fontWeight": "500",  # Slightly bold text for active tab
        "cursor": "pointer",
        "textAlign": "center",  # Center-aligns text in the tab
        "display": "flex",  # Enables flexbox for alignment
        "alignItems": "center",  # Centers content vertically
        "justifyContent": "center",  # Centers content horizontally
        "width": "150px",  # Sets consistent tab width
        "height": "40px",  # Sets consistent tab height
    }

    # Define the container style for the tabs, ensuring it's fixed at the top
    tabs_container_style = {
        "padding": "10px 20px 0 20px",  # Adjusted padding
        "borderBottom": "none",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "backgroundColor": "white",
        "width": "100%",  # Make the width span the full viewport
        "position": "fixed",  # Keeps the container fixed at the top
        "top": "0",  # Ensures it stays at the top of the viewport
        "left": "0",  # Aligns with the left edge of the screen
        "zIndex": "1000",  # Ensures it appears above other content
        "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)",  # Adds a subtle shadow for better visibility
    }

    # Define the main content area style, adding top margin to avoid overlap with tabs
    main_content_style = {
        "marginTop": "100px",  # Adjust the top margin based on the tab container height
        "padding": "10px",  # Add some padding for the main content area
    }

    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname"),
    )
    def display_page(pathname):
        """
        Callback function to render the content of the page based on the selected tab.

        Returns a layout that includes the navigation tabs and the corresponding content
        based on the selected tab.
        """
        return html.Div(
            [
                html.Div(
                    [
                        dcc.Tabs(
                            id="page-1-tabs",
                            value="cluster-tab",  # Default tab is 'cluster-tab'
                            children=[
                                dcc.Tab(
                                    label="Home",
                                    value="cluster-tab",  # Identifier for the cluster analysis tab
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                                dcc.Tab(
                                    label="Entity Analysis",
                                    value="entity-tab",  # Identifier for the entity analysis tab
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                            ],
                            className="custom-tabs",
                            style={
                                "border": "none",
                                "backgroundColor": "transparent",  # No border for the tabs container
                            },
                        ),
                    ],
                    style=tabs_container_style,
                ),
                html.Div(
                    id="tabs-content-page-1", style=main_content_style
                ),  # Main content area
            ]
        )
