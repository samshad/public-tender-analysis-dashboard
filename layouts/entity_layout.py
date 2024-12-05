from dash import html, dcc
import dash_bootstrap_components as dbc


def create_entity_layout(df, min_year, max_year):
    """
        Creates a responsive layout for visualizing and filtering public tender data.
        Includes a sidebar for entity and filter selection, and a main content area
        for various visualizations related to tender analysis, such as frequency count,
        awarded amounts, and topic modeling.
    """
    # Custom style for interactive elements like transitions and pointer cursor
    custom_style = {
        'mark': {
            'transition': 'color 0.3s ease',
            'cursor': 'pointer'
        }
    }


    # Modal for displaying tender details
    description_modal = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Tender Details")),
            dbc.ModalBody(id="modal-body"),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0)
            ),
        ],
        id="tender-modal",
        is_open=False,
        size="lg",
    )

    # Sidebar content, contains filters for cluster, entity, type, and data count
    sidebar_content = dbc.Col(
        [
            html.H4("Filters", className="mb-3"),
            html.H6("Select a cluster:"),
            html.Div([
                html.H6(
                    id='cluster-dropdown-desc',
                    className="mb-2",
                    style={"fontSize": "14px", "color": "#6c757d"}
                ),
                dcc.Dropdown(
                    id='cluster-dropdown',
                    options=[
                        {'label': cluster_name, 'value': cluster_name}
                        for cluster_name in df['ENTITY_CLUSTER_NAME'].unique()
                    ],
                    value=None,
                    placeholder='Select a cluster',
                    clearable=True,
                    searchable=True,
                    optionHeight=60,
                    maxHeight=300,
                    style={
                        'width': '100%',
                    }
                )
            ], style={'max-width': '270px', 'margin-bottom': '1rem'}),

            html.H6("Select an entity:"),
            html.Div([
                html.H6(
                    id='entity-dropdown-desc',
                    className="mb-2",
                    style={"fontSize": "14px", "color": "#6c757d"}
                ),
                dcc.Dropdown(
                    id='entity-dropdown',
                    options=[],  # Updated dynamically based on the selected cluster
                    value=None,
                    placeholder='Select an entity',
                    clearable=True,
                    searchable=True,
                    optionHeight=60,
                    maxHeight=300,
                    style={
                        'width': '100%',
                    }
                )
            ], style={'max-width': '270px', 'margin-bottom': '1rem'}),
            html.H6("Filter by type:", className="mt-3"),
            dbc.Checklist(
                id='filter-checkbox',
                options=[
                    {'label': 'Goods', 'value': 'GOODS'},
                    {'label': 'Service', 'value': 'SERVICE'},
                    {'label': 'Construction', 'value': 'CONSTRUCTION'}
                ],
                value=[],
                labelStyle={'display': 'block', 'margin-bottom': '10px'}
            ),
            html.H6("Number of items:", className="mt-3"),
            html.Div(
                children=[
                    html.H6(
                        "Affect only Tender Frequency Count by Vendor Chart and Vendors by Awarded Amount Chart",
                        className="mb-2",
                        style={"fontSize": "14px", "color": "#6c757d"}
                    ),
                    dcc.Input(
                        id='data-count-input',
                        type='number',
                        value=15,
                        min=1,
                        placeholder='Enter number of items to show',
                        className="w-100 mb-3"
                    ),
                ],
                className="mb-4"  # Optional: adds spacing after the whole filter block
            ),
            html.Div(id='filter-message-warning', className="mt-3"),
        ],
        className="bg-light p-4",
        style={
            "position": "fixed",
            "top": "0",
            "left": "0",
            "bottom": "0",
            "width": "300px",
            "overflow-y": "auto",
            "z-index": "1000",
            "border-right": "1px solid #dee2e6"
        },
        width=3
    )

    # Main content area, contains visualizations and graphs for the tender analysis
    main_content = dbc.Col(
        [

            # Graphs
            dbc.Col(html.H4(id="filter-title-freq-plot-entity"), width=12),
            dcc.Loading(
                id="loading-tender-frequency-count",
                type="circle",
                children=[
                    dcc.Graph(id='tender-frequency-count')
                ]
            ),
            html.Div(id='filter-message-freq-plot'),

            dbc.Col(html.H4(id="filter-title-amount-plot-entity"), width=12),
            dcc.Loading(
                id="loading-awarded-amount-vs-vendor",
                type="circle",
                children=[
                    dcc.Graph(id='awarded-amount-vs-vendor')
                ]
            ),
            html.Div(id='filter-message-amount-plot'),

            dbc.Col(html.H4(id="topic-word-cloud-title-entity"), width=12),
            dcc.Loading(
                id="loading-topic-word-cloud",
                type="circle",
                children=[
                    dcc.Graph(id='topic-word-cloud', config={'displayModeBar': False})
                ]
            ),
            html.Div(id='topic-word-cloud-entity'),

            dbc.Col(html.H4(id="topic-visualization-title-entity"), width=12),
            dcc.Loading(
                id="loading-topic-time-visualization",
                type="circle",
                children=[
                    dcc.Graph(id='topic-time-visualization', config={'displayModeBar': False})
                ]
            ),
            html.Div(id='topic-time-description'),

            dbc.Col(html.H4(id="title-year-award-bar-plot-entity"), width=12),
            dcc.Loading(
                id="loading-year-vs-awarded-amount",
                type="circle",
                children=[
                    dcc.Graph(id='year-vs-awarded-amount', config={'displayModeBar': True})
                ]
            ),
            # Slider for year filtering
            dbc.Row(
                [
                    dbc.Col(
                        dcc.RangeSlider(
                            id='year-slider',
                            min=min_year,
                            max=max_year,
                            value=[min_year, max_year],  # Set as an array
                            marks={str(year): str(year) for year in range(min_year, max_year + 1)}
                        ),
                        width=12
                    ),
                ],
                className="mb-4"
            ),
            html.Div(id='desc-year-award-bar-plot'),
        ],
        className="px-4",
        style={
            "margin-left": "300px",  # Same as sidebar width
            "width": "calc(100% - 300px)",
            "padding-top": "20px"
        },
        width=9
    )

    # Return the layout as a container with sidebar and main content
    return dbc.Container(
        [
            dbc.Row([sidebar_content, main_content]),
            description_modal
        ],
        fluid=False,
        style={"padding": "0"}
    )