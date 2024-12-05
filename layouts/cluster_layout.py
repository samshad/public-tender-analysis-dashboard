from dash import html, dcc
import dash_bootstrap_components as dbc


def create_cluster_layout(df, min_year, max_year, summary_data):
    """
        Creates the layout for the cluster visualization, including the sidebar with filters and
        the main content area with graphs and charts. The layout includes various visualizations
        such as frequency counts, awarded amounts, word clouds, and topic evolution over time.
    """
    custom_style = {
        'mark': {
            'transition': 'color 0.3s ease',
            'cursor': 'pointer'
        }
    }

    # Extract summary data
    total_entities = summary_data["total_entities"]
    total_vendors = summary_data["total_vendors"]
    min_awarded_amount = summary_data["min_awarded_amount"]
    max_awarded_amount = summary_data["max_awarded_amount"]
    min_awarded_year = summary_data["min_awarded_year"]
    max_awarded_year = summary_data["max_awarded_year"]

    # Modal to show tender details
    description_modal = dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Tender Details")),
            dbc.ModalBody(id="modal-body-cluster"),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-modal-cluster", className="ms-auto", n_clicks=0)
            ),
        ],
        id="tender-modal-cluster",
        is_open=False,
        size="lg",
    )

    # Sidebar content layout
    sidebar_content = dbc.Col(
        [
            html.H4("Filters", className="mb-3"),
            html.H6("Select a cluster:"),
            html.Div([
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
            html.H6("Filter by type:", className="mt-3"),
            dbc.Checklist(
                id='filter-checkbox-cluster',
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
                        id='data-count-input-cluster',
                        type='number',
                        value=15,
                        min=1,
                        placeholder='Enter number of items to show',
                        className="w-100 mb-3"
                    ),
                ],
                className="mb-4"  # Optional: adds spacing after the whole filter block
            ),
            html.Div(id='filter-message-warning-cluster', className="mt-3"),

            dbc.Col(html.H5(id="entity-list-field", className="text-center mb-3")),
            html.Div(
                [
                    html.Div(
                        id='entity-list-cluster',
                        className="mt-3",
                        style={
                            "border": "1px solid #ddd",
                            "border-radius": "5px",
                            "padding": "15px",
                            "background-color": "#f8f9fa"
                        }
                    ),
                ],
                id='entity-section-cluster',
                style={'display': 'none'}  # Default is hidden
            ),
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

    static_content_desc_analysis = dbc.Row([
        # Summary Section
        dbc.Row([
            dbc.Col(html.H1("Awarded Public Tenders in Nova Scotia", style={'textAlign': 'center'}), width=12),
        ]),
        dbc.Row([
            dbc.Col(html.H4("Dataset Summary", style={'textAlign': 'center', 'marginBottom': '20px'}), width=12),
        ]),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H5("Unique Entities", className="card-title"),
                    html.P(f"{total_entities:,} entities", className="card-text"),
                ])
            ], style={"backgroundColor": "#e9ecef", "border": "1px solid #dee2e6", "height": "100px"}), width=3),

            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H5("Unique Vendors", className="card-title"),
                    html.P(f"{total_vendors:,} vendors", className="card-text"),
                ])
            ], style={"backgroundColor": "#f1f3f5", "border": "1px solid #dee2e6", "height": "100px"}), width=3),

            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Awarded Amount", className="card-title"),
                        html.P([
                            f"Min: ${min_awarded_amount:,.2f}",
                            html.Br(),  # Adds a line break
                            f"Max: ${max_awarded_amount:,.2f}"
                        ], className="card-text"),
                    ])
                ], style={"backgroundColor": "#edf2f4", "border": "1px solid #dee2e6", "height": "100px"}),
                width=3
            ),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H5("Awarded Year", className="card-title"),
                    html.P(f"Range: {min_awarded_year} - {max_awarded_year}", className="card-text"),
                ])
            ], style={"backgroundColor": "#f8f9fa", "border": "1px solid #dee2e6", "height": "100px"}), width=3),
        ], className="mb-4"),

        # Entity-Year Average Awarded Amount Chart
        dbc.Row([
            dbc.Col(html.H4("How Has the Average Yearly Tender Allocation Evolved Across Different Organizations in Nova Scotia?"), width=12),
            dbc.Col(dcc.Loading(
                id="loading-entity-year-average-amount",
                type="circle",
                children=[
                    dcc.Graph(id='entity-year-average-amount')
                ]
            ), width=12),
            dbc.Col(
                html.P(
                    [
                        "This line graph visualizes the average expenditure on tenders over time (by year) for different public organizations in Nova Scotia, Canada.",
                        html.Ul(
                            [
                                html.Li(
                                    "X-axis (TENDER DATE): This represents the year when funds or awards were accepted."),
                                html.Li(
                                    "Y-axis (TENDER AMOUNT): This shows the average tender expenditure per organization for each year.")
                            ]
                        )
                    ]
                ),
                width=12
            )
        ]),

        # Cluster-Year Average Awarded Amount Chart
        dbc.Row([
            dbc.Col(html.H4("How Do Organization Clusters in Nova Scotia Show Different Spending Patterns Over Time (by Year)?"), width=12),
            dbc.Col(dcc.Loading(
                id="loading-cluster-year-average-amount",
                type="circle",
                children=[
                    dcc.Graph(id='cluster-year-average-amount')
                ]
            ), width=12),
            dbc.Col(
                html.P(
                    [
                        "This visualization displays average tender amounts granted to different organizational clusters in Nova Scotia across multiple years. It reveals funding patterns among various groups—including universities, agencies, municipalities, and education—showing notable spikes and changes that reflect shifting priorities and major projects.",
                        html.Ul(
                            [
                                html.Li(
                                    "X-axis (TENDER DATE): This represents the year when funds or awards were accepted."),
                                html.Li(
                                    "Y-axis (TENDER AMOUNT): This shows the average tender expenditure to each cluster of organizations for each year.")
                            ]
                        )
                    ]
                ),
                width=12
            )

        ]),

        # Cluster-Year Cumulative Awarded Amount Chart
        dbc.Row([
            dbc.Col(html.H4("Which clusters have contributed the most to cumulative tender amounts over the years in Nova Scotia?"), width=12),
            dbc.Col(dcc.Loading(
                id="loading-cluster-year-cumulative-amount",
                type="circle",
                children=[
                    dcc.Graph(id='cluster-year-cumulative-amount')
                ]
            ), width=12),
            dbc.Col(
                html.P(
                    [
                        "This visualization shows the cumulative awarded tender amounts for each cluster of entities over time. It highlights the total contribution of different clusters to tendering activities, emphasizing clusters with significant and consistent growth.",
                        html.Ul(
                            [
                                html.Li(
                                    "X-axis (TENDER DATE): Shows the yearly accumulation of awarded funds."),
                                html.Li(
                                    "Y-axis (TENDER AMOUNT): Displays the total accumulated tender amounts awarded to each cluster over time.")
                            ]
                        )
                    ]
                ),
                width=12
            )
        ])
    ])

    # Main content
    main_content = dbc.Col(
        [
            static_content_desc_analysis,
            # Graphs with Loading Spinners

            dbc.Col(html.H4(id="filter-title-freq-plot-cluster"), width=12),
            dcc.Loading(
                id="loading-tender-frequency-count-cluster",
                type="circle",
                children=[
                    dcc.Graph(id='tender-frequency-count-cluster')
                ]
            ),
            html.Div(id='filter-message-freq-plot-cluster'),

            dbc.Col(html.H4(id="filter-title-amount-plot-cluster"), width=12),
            dcc.Loading(
                id="loading-awarded-amount-vs-vendor-cluster",
                type="circle",
                children=[
                    dcc.Graph(id='awarded-amount-vs-vendor-cluster')
                ]
            ),
            html.Div(id='filter-message-amount-plot-cluster'),

            dbc.Col(html.H4(id="word-cloud-title-cluster"), width=12),
            dcc.Loading(
                id="loading-word-cloud-cluster",
                type="circle",
                children=[
                    dcc.Graph(id='word-cloud-cluster', config={'displayModeBar': False})
                ]
            ),
            html.Div(id='word-cloud-entity-cluster'),

            dbc.Col(html.H4(id="topic-word-cloud-title-cluster"), width=12),
            dcc.Loading(
                id="loading-topic-word-cloud-cluster",
                type="circle",
                children=[
                    dcc.Graph(id='topic-word-cloud-cluster', config={'displayModeBar': False})
                ]
            ),
            html.Div(id='topic-word-cloud-entity-cluster'),

            dbc.Col(html.H4(id="topic-visualization-title-cluster"), width=12),
            dcc.Loading(
                id="loading-topic-time-visualization-cluster",
                type="circle",
                children=[
                    dcc.Graph(id='topic-time-visualization-cluster', config={'displayModeBar': False})
                ]
            ),
            html.Div(id='topic-time-description-cluster'),

            dbc.Col(html.H4(id="title-year-award-bar-plot-cluster"), width=12),
            dcc.Loading(
                id="loading-year-vs-awarded-amount-cluster",
                type="circle",
                children=[
                    dcc.Graph(id='year-vs-awarded-amount-cluster', config={'displayModeBar': True})
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.RangeSlider(
                            id='year-slider-cluster',
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
            html.Div(id='desc-year-award-bar-plot-cluster'),

        ],
        className="px-4",
        style={
            "margin-left": "300px",  # Same as sidebar width
            "width": "calc(100% - 300px)",
            "padding-top": "20px"
        },
        width=12
    )

    # Return the full layout with sidebar, main content, and modal
    return dbc.Container(
        [
            dbc.Row([sidebar_content, main_content]),
            description_modal
        ],
        fluid=False,
        style={"padding": "0"}
    )