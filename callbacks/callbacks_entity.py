import pandas as pd
import dash
import plotly.graph_objects as go
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
    generate_topic_word_cloud_message
)

def register_callbacks_for_entity(app, df, topic_model):
    """
    Registers callbacks to update entity-related visualizations and messages.
    Includes filtering data based on selected entity and cluster, and generating related messages.
    """

    @app.callback(
        Output('entity-dropdown', 'options'),
        Input('cluster-dropdown', 'value')
    )
    def update_entity_dropdown(selected_cluster):
        """
        Updates the entity dropdown options based on the selected cluster.
        Filters the entities belonging to the selected cluster.
        If no cluster is selected, shows all entities.
        """
        if selected_cluster:
            filtered_entities = df[df['ENTITY_CLUSTER_NAME'] == selected_cluster]['ENTITY'].unique()
            return [{'label': entity, 'value': entity} for entity in filtered_entities]
        return [{'label': entity, 'value': entity} for entity in df['ENTITY'].unique()]

    @app.callback(
        [Output('cluster-dropdown-desc', 'children'),
         Output('entity-dropdown-desc', 'children')],
        [Input('entity-dropdown', 'value'),
         Input('cluster-dropdown', 'value')]  # Assuming you have a cluster dropdown with this ID
    )
    def update_message(selected_entity, selected_cluster):
        """
        Updates the messages displayed for the selected entity and cluster.
        Provides relevant information based on whether entity and/or cluster are selected.
        """
        if selected_entity and selected_cluster:
            filtered_df = df[df['ENTITY_CLUSTER_NAME'] == selected_cluster]
            unique_entity_df = filtered_df.drop_duplicates(subset='ENTITY')
            entity_count = len(unique_entity_df)

            return "", f"{selected_entity} belongs to the {selected_cluster} cluster. The {selected_cluster} cluster contains {entity_count} entities."
        elif selected_entity and not selected_cluster:
            # Find the cluster for the selected entity
            cluster_name = df.loc[df['ENTITY'] == selected_entity, 'ENTITY_CLUSTER_NAME']
            filtered_df = df[df['ENTITY_CLUSTER_NAME'] == cluster_name.iloc[0]]
            unique_entity_df = filtered_df.drop_duplicates(subset='ENTITY')
            entity_count = len(unique_entity_df)

            if not cluster_name.empty:
                return "", f"{selected_entity} belongs to the {cluster_name.iloc[0]} cluster. The {selected_cluster} cluster contains {entity_count} entities."
            else:
                return "", ""
        elif selected_cluster and not selected_entity:
            filtered_df = df[df['ENTITY_CLUSTER_NAME'] == selected_cluster]
            unique_entity_df = filtered_df.drop_duplicates(subset='ENTITY')
            entity_count = len(unique_entity_df)
            return "", f"Displaying entities that belong to the {selected_cluster} cluster. The {selected_cluster} cluster contains {entity_count} entities."
        else:
            return (
            "When you select a cluster, the Entity dropdown will display only the entities that belong to the selected cluster.",
            "No cluster is selected, displaying all entities.")

    @app.callback(
        [
            Output('filter-message-warning', 'children'),
            Output('filter-message-freq-plot', 'children'),
            Output('filter-message-amount-plot', 'children'),
            Output('desc-year-award-bar-plot', 'children'),
            Output('topic-word-cloud-entity', 'children'),
        ],
        [
            Input('entity-dropdown', 'value'),
            Input('filter-checkbox', 'value'),
            Input('data-count-input', 'value'),
        ]
    )
    def update_filter_message(selected_entity, selected_filters, data_count):
        """
        Updates the filter-related messages and plots based on the selected entity and filters.
        Displays relevant messages and visualizations after applying filters to the selected entity's data.
        """
        if not selected_entity:
            return html.Span(
                "Please select an entity to display data.",
                style={'color': 'red'}
            ), html.Span(), html.Span(), html.Span(), html.Span()

        filtered_df = df[df['ENTITY'] == selected_entity]

        if not selected_filters:
            return generate_filter_message(
                selected_filters, selected_entity), html.Span(), html.Span(), html.Span(), html.Span()

        for filter_col in selected_filters:
            filtered_df = filtered_df[filtered_df[filter_col] == 1]

        unique_vendors_count = filtered_df['VENDOR'].nunique()

        df_count = len(df)
        filter_df_count = len(filtered_df)

        # Generate the various messages based on the filtered data
        filter_message = generate_filter_message(selected_filters, selected_entity, df_count, filter_df_count)
        vendor_freq_message = generate_vendor_frequency_message(unique_vendors_count, data_count, selected_entity)
        vendor_amount_message = generate_vendor_amount_message(unique_vendors_count, data_count, selected_entity)
        year_award_message = generate_year_award_bar_plot_message(selected_entity)
        topic_word_cloud_message = generate_topic_word_cloud_message(unique_vendors_count, selected_entity)

        return filter_message, vendor_freq_message, vendor_amount_message, year_award_message, topic_word_cloud_message

    @app.callback(
        [
            Output('filter-title-freq-plot-entity', 'children'),
            Output('filter-title-amount-plot-entity', 'children'),
            Output('title-year-award-bar-plot-entity', 'children'),
            Output('topic-word-cloud-title-entity', 'children'),
            Output('topic-visualization-title-entity', 'children'),
        ],
        [
            Input('entity-dropdown', 'value'),
        ]
    )
    def update_title(selected_entity):
        """
        Updates the filter messages and visualizations based on the selected cluster and filters.
        Ensures appropriate filtering of data and generates the corresponding messages.
        """

        # If no cluster is selected, show a warning message
        if not selected_entity:
            return html.Span(), html.Span(), html.Span(), html.Span(), html.Span()

        # Assign titles to variables
        freq_plot_title = f"Which Vendors Have the Most Frequent Tender Awards in {selected_entity}?"
        amount_plot_title = f"Which vendors have received the highest total awarded amounts in {selected_entity}?"
        desc_plot_title = f"How are tender amounts distributed by size, vendor, and year in {selected_entity}, and which vendors or tenders stand out when examining detailed information in pop-ups?"
        topic_word_cloud_title = f"What are the key topics and frequently recurring themes in tender descriptions for {selected_entity}, as identified through topic modeling?"
        topic_visualization_title = f"How have the topics in tender descriptions evolved over time for {selected_entity}, and what trends or shifts can be identified?"

        # Return the titles to the respective outputs
        return freq_plot_title, amount_plot_title, desc_plot_title, topic_word_cloud_title, topic_visualization_title

    @app.callback(
        [
            Output('tender-frequency-count', 'figure'),
            Output('awarded-amount-vs-vendor', 'figure'),
            Output('year-vs-awarded-amount', 'figure'),
        ],
        [
            Input('entity-dropdown', 'value'),
            Input('filter-checkbox', 'value'),
            Input('data-count-input', 'value'),
            Input('year-slider', 'value'),
        ]
    )
    def update_all_bar_charts(selected_entity, selected_filters, data_count, selected_years):
        """
        Updates the visualizations for tender frequency, awarded amounts by vendor,
        and awarded amounts over the selected years.
        Filters the data based on the selected entity and other filter criteria,
        then generates three bar charts.
        """

        # Return empty figures if required inputs are missing
        if not selected_entity or not selected_filters or not selected_years:
            return go.Figure(), go.Figure(), go.Figure()

        # Filter the dataset based on the selected entity and filters
        filtered_df = df[df['ENTITY'] == selected_entity]
        for filter_col in selected_filters:
            filtered_df = filtered_df[filtered_df[filter_col] == 1]

        # Create the tender frequency bar chart
        tender_frequency_figure = go.Figure()
        if not filtered_df.empty:
            tender_frequency = filtered_df['VENDOR'].value_counts().reset_index()
            tender_frequency.columns = ['VENDOR', 'FREQUENCY']
            tender_frequency_figure = create_tender_frequency_bar_chart(
                tender_frequency, data_count, 'VENDOR', 'FREQUENCY')

        # Create the awarded amount vs vendor bar chart
        awarded_amount_figure = go.Figure()
        if not filtered_df.empty:
            awarded_amount = filtered_df.groupby('VENDOR')['AWARDED_AMOUNT'].sum().reset_index()
            awarded_amount = awarded_amount.sort_values(by='AWARDED_AMOUNT', ascending=False).head(data_count)
            awarded_amount_figure = create_awarded_amount_vs_vendor_or_entity_bar_chart(
                awarded_amount, data_count, 'VENDOR', 'AWARDED_AMOUNT')

        # Create the year vs awarded amount bar chart
        year_awarded_amount_figure = go.Figure()
        if not filtered_df.empty:
            filtered_df_year = filtered_df[
                (filtered_df['TENDER_START_DATE'].dt.year >= selected_years[0]) &
                (filtered_df['TENDER_START_DATE'].dt.year <= selected_years[1])
                ]
            if not filtered_df_year.empty:
                # Prepare data for individual tenders
                tender_data = filtered_df_year[['TENDER_START_DATE', 'AWARDED_AMOUNT', 'VENDOR', 'TENDER_ID', 'ENTITY_CLUSTER_NAME']].dropna()

                # Create a list to store bar data
                bar_data = []

                for _, row in tender_data.iterrows():
                    start_year = row['TENDER_START_DATE'].year

                    # Add the entire tender amount to the start year
                    bar_data.append({
                        'YEAR': start_year,
                        'AWARDED_AMOUNT': row['AWARDED_AMOUNT'],
                        'VENDOR': row['VENDOR'],
                        'TENDER_ID': row['TENDER_ID'],
                        'ENTITY_CLUSTER_NAME': row['ENTITY_CLUSTER_NAME']
                    })

                # Convert to DataFrame
                bar_df = pd.DataFrame(bar_data)

                # Group by Year and Vendor, summing awarded amounts
                grouped_df = bar_df.groupby(['TENDER_ID', 'YEAR', 'VENDOR', 'ENTITY_CLUSTER_NAME'])['AWARDED_AMOUNT'].sum().reset_index()

                # Sort by Vendor and Year
                grouped_df = grouped_df.sort_values(by=['VENDOR', 'YEAR'],
                                                    key=lambda col: col.str.lower() if col.name == 'VENDOR' else col)

                year_awarded_amount_figure = create_year_vs_awarded_amount_bar_chart(grouped_df, 'VENDOR')

        # Return all three figures
        return tender_frequency_figure, awarded_amount_figure, year_awarded_amount_figure

    @app.callback(
        [Output("modal-body", "children"), Output("tender-modal", "is_open"),
         Output("year-vs-awarded-amount", "clickData")],
        [
            Input("year-vs-awarded-amount", "clickData"),
            Input("close-modal", "n_clicks")
        ],
        [State("tender-modal", "is_open")],  # Track the current state of the modal
        prevent_initial_call=True
    )
    def toggle_modal(bar_clickData, n_clicks, is_open):
        """
        Handles the modal display when a bar chart is clicked to show tender details.
        If the close button is clicked, the modal will close.
        """

        ctx = dash.callback_context  # Get the triggered context
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]  # Get the ID of the triggered component

        # If the close button is clicked, close the modal and reset clickData
        if triggered_id == "close-modal" and n_clicks:
            return "", False, None  # Close the modal and reset clickData

        # Handle click data from the chart
        if triggered_id == "year-vs-awarded-amount" and bar_clickData:
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
        Output('topic-word-cloud', 'figure'),
        [
            Input('entity-dropdown', 'value'),
            Input('filter-checkbox', 'value'),
        ]
    )
    def update_topic_word_cloud(selected_entity, selected_filters):
        """
        Updates the topic-based word cloud visualization based on the selected entity and filter criteria.
        Filters the dataset by entity and selected filters, performs topic modeling, and generates a word cloud of topics.
        """
        if not selected_entity or not selected_filters:
            return go.Figure()  # Return empty figure if no entity or filter is selected

        filtered_df = df[df['ENTITY'] == selected_entity]
        for filter_col in selected_filters:
            filtered_df = filtered_df[filtered_df[filter_col] == 1]  # Apply selected filters

        # Ensure there are enough samples
        unique_descriptions = filtered_df['TENDER_DESCRIPTION'].dropna().unique()
        if len(unique_descriptions) < 2:  # Minimum of two unique descriptions required
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

        # Generate word cloud text based on the topics
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

        return create_word_cloud(wordcloud_text)

    @app.callback(
        [Output('topic-time-visualization', 'figure'),
         Output('topic-time-description', 'children')],
        [
            Input('entity-dropdown', 'value'),
            Input('filter-checkbox', 'value'),
        ]
    )
    def update_topic_time_visualization(selected_entity, selected_filters):
        """
        Updates the visualization of topics over time (based on awarded year) for the selected entity.
        Ensures there are enough tender descriptions and applies topic modeling to visualize topic distribution over time.
        """

        # Check if selected_entity and selected_filters are provided; return empty figure if not.
        if not selected_entity or not selected_filters:
            return go.Figure(), ""

        # Filter the dataframe based on selected entity and filters
        filtered_df = df[df['ENTITY'] == selected_entity]
        for filter_col in selected_filters:
            filtered_df = filtered_df[filtered_df[filter_col] == 1]

        # Ensure there are enough tender descriptions to proceed
        unique_descriptions = filtered_df['TENDER_DESCRIPTION'].dropna().unique()

        # If there are fewer than 2 unique tender descriptions, return a message
        if len(unique_descriptions) < 2:  # Minimum of two unique samples required
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

        # Extract the 'year' from 'AWARDED_DATE' to analyze topics over time
        filtered_df['AWARDED_YEAR'] = pd.to_datetime(filtered_df['AWARDED_DATE'], errors='coerce').dt.year

        # Try fitting the BERTopic model and handle potential errors
        try:
            topics, _ = topic_model.fit_transform(filtered_df['TENDER_DESCRIPTION'])
            filtered_df['TOPIC'] = topics
        except Exception as e:
            return return_empty_plot(), ""

        # Group the data by awarded year and topic, and count occurrences
        topic_counts = filtered_df.groupby(['AWARDED_YEAR', 'TOPIC']).size().unstack(fill_value=0)

        # Retrieve keywords for each topic for better visualization
        topic_keywords = {}
        for topic_num in topic_counts.columns:
            topic_keywords[topic_num] = ', '.join([word[0] for word in topic_model.get_topic(topic_num)])

        # Return the topic time visualization and the associated keywords for the selected entity
        return create_topic_time_visualization(topic_counts, topic_keywords, selected_entity)




