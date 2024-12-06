import pandas as pd
import dash
import plotly.graph_objects as go
import plotly.express as px
from dash import html, Input, Output, State

from utils.error_handling import return_empty_plot
from visualizations.tender_frequency import create_tender_frequency_bar_chart
from visualizations.topic_time_visualization import create_topic_time_visualization
from visualizations.vendor_or_entity_vs_awarded_amounts import create_awarded_amount_vs_vendor_or_entity_bar_chart
from visualizations.wordcloud import create_word_cloud
from visualizations.year_vs_awarded_amount import create_year_vs_awarded_amount_bar_chart
from visualizations.messages_entity_analysis import (
    generate_filter_message,
    generate_vendor_frequency_message,
    generate_vendor_amount_message,
    generate_year_award_bar_plot_message,
    generate_general_word_cloud_message,
    generate_topic_word_cloud_message
)

def register_callbacks_for_cluster(app, df, topic_model):
    """
        Registers callbacks to update various plots for descriptive analysis of awarded amounts.
        Includes Entity-Year and Cluster-Year visualizations for both average and cumulative amounts.
        """

    def prepare_entity_year_avg(df):
        """Prepares data for the Entity-Year Average Awarded Amount plot."""
        # Grouping by entity and awarded year, calculating the mean of the awarded amount
        data = (df[['AWARDED_AMOUNT']]
                .groupby([df.ENTITY, df['AWARDED_DATE'].dt.year])
                .mean().reset_index())
        data.columns = ['ENTITY', 'AWARDED_DATE', 'AWARDED_AMOUNT']
        return data

    def prepare_cluster_year_avg(df):
        """Prepares data for the Cluster-Year Average Awarded Amount plot."""
        # Grouping by entity cluster and awarded year, calculating the mean of the awarded amount
        data = (df[['AWARDED_AMOUNT']]
                .groupby([df.ENTITY_CLUSTER_NAME, df['AWARDED_DATE'].dt.year])
                .mean().reset_index())
        data.columns = ['ENTITY_CLUSTER_NAME', 'AWARDED_DATE', 'AWARDED_AMOUNT']
        return data

    def prepare_cluster_year_cumulative(df):
        """Prepares data for the Cluster-Year Cumulative Awarded Amount plot."""
        # Grouping by entity cluster and awarded year, calculating the sum, then cumulative sum
        data = (df[['AWARDED_AMOUNT']]
                .groupby([df.ENTITY_CLUSTER_NAME, df['AWARDED_DATE'].dt.year])
                .sum()
                .groupby(level=0).cumsum().reset_index())
        data.columns = ['ENTITY_CLUSTER_NAME', 'AWARDED_DATE', 'AWARDED_AMOUNT']
        return data

    @app.callback(
        [
            Output('entity-year-average-amount', 'figure'),
            Output('cluster-year-average-amount', 'figure'),
            Output('cluster-year-cumulative-amount', 'figure'),
        ],
        [
            Input('entity-year-average-amount', 'id'),
            Input('cluster-year-average-amount', 'id'),
            Input('cluster-year-cumulative-amount', 'id')
        ]
    )
    def update_entity_tender_frequency(x, y, z):
        """
        Updates the visualizations for Entity-Year and Cluster-Year awarded amounts (both average and cumulative).
        Each plot is generated using the respective data preparation functions.
        """

        # Entity-Year Average Awarded Amount Plot
        entity_year_avg = prepare_entity_year_avg(df)
        fig_entity_avg = px.line(
            entity_year_avg,
            x='AWARDED_DATE',
            y='AWARDED_AMOUNT',
            color='ENTITY',
            labels={
                'AWARDED_DATE': 'TENDER DATE',
                'AWARDED_AMOUNT': 'TENDER AMOUNT'
            }
        )

        # Cluster-Year Average Awarded Amount Plot
        cluster_year_avg = prepare_cluster_year_avg(df)
        fig_cluster_avg = px.line(
            cluster_year_avg,
            x='AWARDED_DATE',
            y='AWARDED_AMOUNT',
            color='ENTITY_CLUSTER_NAME',
            labels={
                'AWARDED_DATE': 'TENDER DATE',
                'AWARDED_AMOUNT': 'TENDER AMOUNT'
            }
        )

        # Cluster-Year Cumulative Awarded Amount Plot
        cluster_year_cumulative = prepare_cluster_year_cumulative(df)
        fig_cluster_cum = px.line(
            cluster_year_cumulative,
            x='AWARDED_DATE',
            y='AWARDED_AMOUNT',
            color='ENTITY_CLUSTER_NAME',
            labels={
                'AWARDED_DATE': 'TENDER DATE',
                'AWARDED_AMOUNT': 'TENDER AMOUNT'
            }
        )

        return fig_entity_avg, fig_cluster_avg, fig_cluster_cum

    """
    Registers Dash callbacks for updating cluster-related visualizations based on user input.
    Filters and processes data based on the selected cluster and other user inputs (filters, data count).
    """
    @app.callback(
        [
            Output('filter-message-warning-cluster', 'children'),
            Output('filter-message-freq-plot-cluster', 'children'),
            Output('filter-message-amount-plot-cluster', 'children'),
            Output('desc-year-award-bar-plot-cluster', 'children'),
            Output('word-cloud-entity-cluster', 'children'),
            Output('topic-word-cloud-entity-cluster', 'children'),
        ],
        [
            Input('cluster-dropdown', 'value'),
            Input('filter-checkbox-cluster', 'value'),
            Input('data-count-input-cluster', 'value'),
        ]
    )
    def update_filter_message(selected_cluster, selected_filters, data_count):
        """
        Updates the filter messages and visualizations based on the selected cluster and filters.
        Ensures appropriate filtering of data and generates the corresponding messages.
        """

        # If no cluster is selected, show a warning message
        if not selected_cluster:
            return html.Span(
                "Please select a cluster to display more data.",
                style={'color': 'red'}
            ), html.Span(), html.Span(), html.Span(), html.Span(), html.Span()

        # Filter the DataFrame by the selected cluster
        filtered_df = df[df['ENTITY_CLUSTER_NAME'] == selected_cluster]

        # If no filters are selected, return a default filter message
        if not selected_filters:
            return generate_filter_message(
                selected_filters, selected_cluster), html.Span(), html.Span(), html.Span(), html.Span(), html.Span()

        # Apply selected filters to the data
        for filter_col in selected_filters:
            filtered_df = filtered_df[filtered_df[filter_col] == 1]

        # Count unique vendors in the filtered dataset
        unique_vendors_count = filtered_df['VENDOR'].nunique()

        df_count = len(df)
        filter_df_count = len(filtered_df)

        # Prepare messages for different visualizations
        filter_message = generate_filter_message(selected_filters, selected_cluster, df_count, filter_df_count)
        vendor_freq_message = generate_vendor_frequency_message(unique_vendors_count, data_count, selected_cluster, True)
        vendor_amount_message = generate_vendor_amount_message(unique_vendors_count, data_count, selected_cluster, True)
        year_award_message = generate_year_award_bar_plot_message(selected_cluster, True)
        general_word_cloud_message = generate_general_word_cloud_message(unique_vendors_count, selected_cluster, True)
        topic_word_cloud_message = generate_topic_word_cloud_message(unique_vendors_count, selected_cluster, True)

        # Return all the generated messages to update the UI components
        return filter_message, vendor_freq_message, vendor_amount_message, year_award_message, general_word_cloud_message, topic_word_cloud_message

    @app.callback(
        [
            Output('filter-title-freq-plot-cluster', 'children'),
            Output('filter-title-amount-plot-cluster', 'children'),
            Output('title-year-award-bar-plot-cluster', 'children'),
            Output('word-cloud-title-cluster', 'children'),
            Output('topic-word-cloud-title-cluster', 'children'),
            Output('topic-visualization-title-cluster', 'children'),
            Output('entity-list-field', 'children'),
        ],
        [
            Input('cluster-dropdown', 'value'),
        ]
    )
    def update_title(selected_cluster):
        """
        Updates the filter messages and visualizations based on the selected cluster and filters.
        Ensures appropriate filtering of data and generates the corresponding messages.
        """

        # If no cluster is selected, show a warning message
        if not selected_cluster:
            return html.Span(), html.Span(), html.Span(), html.Span(), html.Span(), html.Span(), html.Span()

        # Assign titles to variables
        freq_plot_title = f"Which Vendors Have the Most Frequent Tender Awards in the {selected_cluster} Cluster?"
        amount_plot_title = f"Which vendors have received the highest total awarded amounts in the {selected_cluster} cluster?"
        desc_plot_title = f"How are tender amounts distributed by size, vendor, and year in the {selected_cluster} cluster, and which vendors or tenders stand out when examining detailed information in pop-ups?"
        word_cloud_title = f"What are the most common themes and key terms in tender descriptions for the {selected_cluster} cluster, and how do they reflect the universities' procurement priorities?"
        topic_word_cloud_title = f"What are the key topics and frequently recurring themes in tender descriptions for the {selected_cluster} cluster, as identified through topic modeling?"
        topic_visualization_title = f"How have the topics in tender descriptions evolved over time for the {selected_cluster} cluster, and what trends or shifts can be identified?"

        # Filter the DataFrame by the selected cluster
        filtered_df = df[df['ENTITY_CLUSTER_NAME'] == selected_cluster]

        unique_entity_df = filtered_df.drop_duplicates(subset='ENTITY')
        entity_count = len(unique_entity_df)

        entity_list_message = html.Span(
            f"The {selected_cluster} contains {entity_count} entities, "
            f"as listed below: ",
            style={'color': 'green'}
        )
        # Return the titles to the respective outputs
        return freq_plot_title, amount_plot_title, desc_plot_title, word_cloud_title, topic_word_cloud_title, topic_visualization_title, entity_list_message

    @app.callback(
        [Output('entity-list-cluster', 'children'),
         Output('entity-section-cluster', 'style')],
        [Input('cluster-dropdown', 'value')]
    )
    def update_entity_list(selected_cluster):
        """
        Updates the list of entities based on the selected cluster.
        If a cluster is selected, the corresponding entities are displayed.
        If no cluster is selected, the entity list is hidden.
        """
        if selected_cluster:
            # Filter the entities that belong to the selected cluster
            entities_in_cluster = df[df['ENTITY_CLUSTER_NAME'] == selected_cluster]['ENTITY'].unique()

            # Create a list of entities to display
            entity_list = html.Ul([html.Li(entity) for entity in entities_in_cluster])

            # Return the entity list and set the section style to display it
            return entity_list, {'display': 'block'}
        else:
            # Return None and hide the section if no cluster is selected
            return None, {'display': 'none'}

    @app.callback(
        [
            Output('tender-frequency-count-cluster', 'figure'),
            Output('awarded-amount-vs-vendor-cluster', 'figure'),
            Output('year-vs-awarded-amount-cluster', 'figure'),
        ],
        [
            Input('cluster-dropdown', 'value'),
            Input('filter-checkbox-cluster', 'value'),
            Input('data-count-input-cluster', 'value'),
            Input('year-slider-cluster', 'value'),
        ]
    )
    def update_all_bar_charts(selected_cluster, selected_filters, data_count, selected_years):
        """
        Updates all the bar charts based on the selected cluster, filters, data count, and year range.
        Creates and returns figures for:
        - Tender frequency by vendor
        - Awarded amount by vendor
        - Awarded amount vs year
        """
        # Return empty figures if the necessary inputs are missing
        if not selected_cluster or not selected_filters or not selected_years:
            return go.Figure(), go.Figure(), go.Figure()

        # Filter the dataframe based on the selected cluster
        filtered_df = df[df['ENTITY_CLUSTER_NAME'] == selected_cluster]

        # Apply selected filters to the data
        for filter_col in selected_filters:
            filtered_df = filtered_df[filtered_df[filter_col] == 1]

        # Create the tender frequency bar chart
        tender_frequency_figure = go.Figure()
        if not filtered_df.empty:
            # Count the frequency of tenders by vendor
            tender_frequency = filtered_df['VENDOR'].value_counts().reset_index()
            tender_frequency.columns = ['VENDOR', 'FREQUENCY']

            # Create and assign the tender frequency chart
            tender_frequency_figure = create_tender_frequency_bar_chart(
                tender_frequency, data_count, 'VENDOR', 'FREQUENCY')

        # Create the awarded amount vs vendor bar chart
        awarded_amount_figure = go.Figure()
        if not filtered_df.empty:
            # Calculate total awarded amount by vendor
            awarded_amount = filtered_df.groupby('VENDOR')['AWARDED_AMOUNT'].sum().reset_index()
            awarded_amount = awarded_amount.sort_values(by='AWARDED_AMOUNT', ascending=False).head(data_count)

            # Create and assign the awarded amount vs vendor chart
            awarded_amount_figure = create_awarded_amount_vs_vendor_or_entity_bar_chart(
                awarded_amount, data_count, 'VENDOR', 'AWARDED_AMOUNT')

        # Create the year vs awarded amount bar chart
        year_awarded_amount_figure = go.Figure()
        if not filtered_df.empty:
            # Filter data for the selected year range
            filtered_df_year = filtered_df[
                (filtered_df['TENDER_START_DATE'].dt.year >= selected_years[0]) &
                (filtered_df['TENDER_START_DATE'].dt.year <= selected_years[1])
                ]

            if not filtered_df_year.empty:
                # Prepare data for tenders, including tender year and awarded amount
                tender_data = filtered_df_year[['TENDER_START_DATE', 'AWARDED_AMOUNT', 'VENDOR', 'TENDER_ID', 'ENTITY_CLUSTER_NAME']].dropna()

                # Create a list to store tender data for each year
                bar_data = []
                for _, row in tender_data.iterrows():
                    start_year = row['TENDER_START_DATE'].year
                    bar_data.append({
                        'YEAR': start_year,
                        'AWARDED_AMOUNT': row['AWARDED_AMOUNT'],
                        'VENDOR': row['VENDOR'],
                        'TENDER_ID': row['TENDER_ID'],
                        'ENTITY_CLUSTER_NAME': row['ENTITY_CLUSTER_NAME']
                    })

                # Convert the list to a DataFrame
                bar_df = pd.DataFrame(bar_data)

                # Group by Year and Vendor, summing the awarded amounts
                grouped_df = bar_df.groupby(['TENDER_ID', 'YEAR', 'VENDOR', 'ENTITY_CLUSTER_NAME'])['AWARDED_AMOUNT'].sum().reset_index()

                # Sort by Vendor and Year
                grouped_df = grouped_df.sort_values(by=['VENDOR', 'YEAR'],
                                                    key=lambda col: col.str.lower() if col.name == 'VENDOR' else col)

                # Create and assign the year vs awarded amount chart
                year_awarded_amount_figure = create_year_vs_awarded_amount_bar_chart(grouped_df, 'VENDOR')

        # Return all three figures
        return tender_frequency_figure, awarded_amount_figure, year_awarded_amount_figure

    @app.callback(
        [
            Output("modal-body-cluster", "children"),
            Output("tender-modal-cluster", "is_open"),
            Output("year-vs-awarded-amount-cluster", "clickData")  # Reset clickData
        ],
        [
            Input("year-vs-awarded-amount-cluster", "clickData"),
            Input("close-modal-cluster", "n_clicks")
        ],
        [State("tender-modal-cluster", "is_open")],  # Track the current state of the modal
        prevent_initial_call=True
    )
    def toggle_modal(bar_clickData, n_clicks, is_open):
        """
        Toggles the visibility of the modal and updates its content based on user interaction.
        Handles clicks on the chart and the close button, displaying detailed information for the selected tender.
        """
        ctx = dash.callback_context  # Get the triggered context
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]  # Get the ID of the triggered component

        # If the close button is clicked, close the modal and reset clickData
        if triggered_id == "close-modal-cluster" and n_clicks:
            return "", False, None  # Close the modal and reset clickData

        # Handle click data from the chart
        if triggered_id == "year-vs-awarded-amount-cluster" and bar_clickData:
            tender_id = bar_clickData["points"][0]["customdata"][0]
            # Filter the dataframe for the clicked year and vendor
            selected_tender = df[df["TENDER_ID"] == tender_id]

            # If the selected tender exists, extract its details
            if not selected_tender.empty:
                tender_description = selected_tender.iloc[0]["TENDER_DESCRIPTION"]
                tender_duration = (selected_tender.iloc[0]["TENDER_CLOSE_DATE"] - selected_tender.iloc[0][
                    "TENDER_START_DATE"]).days
                awarded_date = selected_tender.iloc[0]["AWARDED_DATE"].strftime("%Y-%m-%d")  # Format date
                vendor_name = selected_tender.iloc[0]["VENDOR"]
                entity_name = selected_tender.iloc[0]["ENTITY"]

                # Set modal content
                modal_content = [
                    html.P(f"Tender Description: {tender_description}"),
                    html.P(f"Tender Duration: {tender_duration} days"),
                    html.P(f"Tender Awarded Date: {awarded_date}"),
                    html.P(f"Vendor: {vendor_name}"),
                    html.P(f"Entity: {entity_name}")
                ]
                return modal_content, True, bar_clickData  # Open modal with content and preserve clickData

        # If no valid clickData is present, or the modal is already open, return existing state
        return "", is_open, bar_clickData

    @app.callback(
        Output('word-cloud-cluster', 'figure'),
        [
            Input('cluster-dropdown', 'value'),
            Input('filter-checkbox-cluster', 'value'),
        ]
    )
    def update_word_cloud(selected_cluster, selected_filters):
        """
        Updates the word cloud visualization based on the selected cluster and filters.
        Filters the data and generates a word cloud from the tender descriptions.
        """
        if not selected_cluster or not selected_filters:
            return go.Figure()  # Return an empty figure if no cluster or filters are selected

        filtered_df = df[df['ENTITY_CLUSTER_NAME'] == selected_cluster]
        for filter_col in selected_filters:
            filtered_df = filtered_df[filtered_df[filter_col] == 1]

        text = ' '.join(filtered_df['TENDER_DESCRIPTION'])

        if not text.strip():  # Check if text is just whitespace
            return go.Figure()  # Return an empty figure if no valid text is available

        return create_word_cloud(text)  # Generate the word cloud

    @app.callback(
        Output('topic-word-cloud-cluster', 'figure'),
        [
            Input('cluster-dropdown', 'value'),
            Input('filter-checkbox-cluster', 'value'),
        ]
    )
    def update_topic_word_cloud(selected_cluster, selected_filters):
        """
        Updates the topic-based word cloud visualization, applying topic modeling (BERTopic) on tender descriptions.
        Filters the data, performs topic modeling, and visualizes the most frequent words across topics.
        """
        if not selected_cluster or not selected_filters:
            return go.Figure()  # Return an empty figure if no cluster or filters are selected

        filtered_df = df[df['ENTITY_CLUSTER_NAME'] == selected_cluster]
        for filter_col in selected_filters:
            filtered_df = filtered_df[filtered_df[filter_col] == 1]

        # Ensure there are enough samples for topic modeling
        unique_descriptions = filtered_df['TENDER_DESCRIPTION'].dropna().unique()
        if len(unique_descriptions) < 2:  # Minimum of two unique samples required for topic modeling
            return go.Figure().update_layout(
                annotations=[{
                    'text': "Not enough topics to generate a word cloud. Try selecting more filters or another entity.",
                    'xref': 'paper', 'yref': 'paper',
                    'x': 0.5, 'y': 0.5,
                    'xanchor': 'center', 'yanchor': 'middle',
                    'showarrow': False,
                    'font': {'size': 16, 'color': 'red'}
                }]
            )

        # Try fitting the BERTopic model and handle potential errors
        try:
            topics, _ = topic_model.fit_transform(filtered_df['TENDER_DESCRIPTION'])
            filtered_df['TOPIC'] = topics
        except Exception as e:
            return return_empty_plot()

        # Collect the most frequent words across all topics
        topic_nums = filtered_df['TOPIC'].unique()
        words = []
        for topic_num in topic_nums:
            topic_words = topic_model.get_topic(topic_num)
            if topic_words:  # Handle empty topics gracefully
                words.extend(topic_words)

        wordcloud_text = ' '.join([word[0] for word in words])
        if not wordcloud_text.strip():  # Check if text is just whitespace
            return go.Figure().update_layout(
                annotations=[{
                    'text': "Not enough topics to generate a word cloud. Try selecting more filters or another entity.",
                    'xref': 'paper', 'yref': 'paper',
                    'x': 0.5, 'y': 0.5,
                    'xanchor': 'center', 'yanchor': 'middle',
                    'showarrow': False,
                    'font': {'size': 16, 'color': 'red'}
                }]
            )

        return create_word_cloud(wordcloud_text)  # Generate the word cloud for topics

    @app.callback(
        [Output('topic-time-visualization-cluster', 'figure'),
         Output('topic-time-description-cluster', 'children')],
        [
            Input('cluster-dropdown', 'value'),
            Input('filter-checkbox-cluster', 'value'),
        ]
    )
    def update_topic_time_visualization(selected_cluster, selected_filters):
        """
        Updates the topic visualization over time (based on awarded year) for the selected cluster.
        Ensures enough tender descriptions are present, fits a BERTopic model, and visualizes the topic distribution over time.
        """
        if not selected_cluster or not selected_filters:
            return go.Figure(), ""

        # Filter dataframe based on the selected cluster and filters
        filtered_df = df[df['ENTITY_CLUSTER_NAME'] == selected_cluster]
        for filter_col in selected_filters:
            filtered_df = filtered_df[filtered_df[filter_col] == 1]

        # Ensure there are enough tender descriptions to proceed
        unique_descriptions = filtered_df['TENDER_DESCRIPTION'].dropna().unique()
        if len(unique_descriptions) < 2:  # Minimum of two unique descriptions required
            return go.Figure().update_layout(
                annotations=[{
                    'text': "Not enough tender descriptions to visualize topics over time. Please select more data.",
                    'xref': 'paper', 'yref': 'paper',
                    'x': 0.5, 'y': 0.5,
                    'xanchor': 'center', 'yanchor': 'middle',
                    'showarrow': False,
                    'font': {'size': 16, 'color': 'red'}
                }]
            ), ""

        # Extract the 'year' from the 'AWARDED_DATE'
        filtered_df['AWARDED_YEAR'] = pd.to_datetime(filtered_df['AWARDED_DATE'], errors='coerce').dt.year

        # Try fitting the BERTopic model and handle potential errors
        try:
            topics, _ = topic_model.fit_transform(filtered_df['TENDER_DESCRIPTION'])
            filtered_df['TOPIC'] = topics
        except Exception as e:
            return return_empty_plot(), ""

        # Count topic occurrences by awarded year
        topic_counts = filtered_df.groupby(['AWARDED_YEAR', 'TOPIC']).size().unstack(fill_value=0)

        # Prepare topic keywords for display
        topic_keywords = {}
        for topic_num in topic_counts.columns:
            topic_keywords[topic_num] = ', '.join([word[0] for word in topic_model.get_topic(topic_num)])

        # Generate the topic-time visualization chart
        return create_topic_time_visualization(topic_counts, topic_keywords, selected_cluster, True)
