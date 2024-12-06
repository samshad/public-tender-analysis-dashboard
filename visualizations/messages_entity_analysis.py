from dash import html

def generate_filter_message(selected_filters, selected_item, df_count = 0, filters_df_count = 0):
    if not selected_filters:
        return html.Span(
            "Please select one or more categories to display data.",
            style={'color': 'red'}
        )

    return html.Span(
        f"selected {', '.join(selected_filters).lower()}, so you can see only where"
        f" {' and '.join(selected_filters).lower()} from {selected_item}.\n"
        f"Filtered {filters_df_count} tenders from a total of {df_count} tenders.\n",
        style={'color': 'black', 'whiteSpace': 'pre-line'}
    )

def generate_vendor_count_message(selected_entity, unique_vendors_count, data_count):
    return f"{selected_entity} contains {unique_vendors_count} unique-vendor tenders with the applied filters. Showing {data_count} of them."


def generate_vendor_frequency_message(unique_vendors_count, data_count, selected_item, is_cluster=False):
    if is_cluster:
        item_message = f"within the {selected_item} cluster"
    else:
        item_message = f"within the {selected_item} organization"

    return html.Div(
        children=[
            html.P(
                f"There are {unique_vendors_count} unique-vendor tenders with the selected filters. "
                f"This bar chart shows {data_count} of those vendors who have received the most tender awards {item_message}. "
                "The vendors are ranked by the number of tenders they won, revealing which companies have been most successful in securing university contracts."
            ),
            html.Ul(
                [
                    html.Li("X-axis (VENDOR): Shows the company names that received tender awards."),
                    html.Li("Y-axis (FREQUENCY): Shows the count of tenders awarded to each vendor.")
                ]
            )
        ],
        style={'color': 'black'}
    )


def generate_vendor_amount_message(unique_vendors_count, data_count, selected_item, is_cluster=False):
    if is_cluster:
        item_message = f"within the {selected_item} cluster"
    else:
        item_message = f"within the {selected_item} organization"

    return html.Div(
        children=[
            html.P(
                f"There are {unique_vendors_count} unique-vendor tenders with the selected filters. This bar chart highlights the top"
                f" {data_count} vendors based on their total awarded tender amounts {item_message}. It identifies"
                f" vendors with the largest financial awards, sorted by the total awarded amount."
            ),
            html.Ul(
                [
                    html.Li("X-axis (VENDOR): Represents the names of vendors awarded tenders."),
                    html.Li("Y-axis (AWARDED_AMOUNT): Indicates the total monetary value of tenders awarded to each vendor.")
                ]
            )
        ],
        style={'color': 'black'}
    )


def generate_year_award_bar_plot_message(selected_item, is_cluster=False):
    if is_cluster:
        item_message_one = f"in the {selected_item} cluster"
        item_message_two = f"within the {selected_item} cluster"
    else:
        item_message_one = f"in the {selected_item} organization"
        item_message_two = f"within the {selected_item} organization"

    return html.Div(
        children=[
            html.P(
                f"This stacked bar chart displays the total awarded tender amounts by year for various vendors"
                f" {item_message_one}. It highlights yearly trends in vendor participation and awarded amounts,"
                f" enabling comparisons across vendors over time and identifying peak years for tender awards. This"
                f" visualization helps us see each vendor's total awarded amount by year, providing insight into yearly"
                f" trends in vendor awards {item_message_two}."
            ),
            html.Ul(
                [
                    html.Li("X-axis (YEAR): Represents the year of tender awards."),
                    html.Li("Y-axis (AWARDED AMOUNT): Indicates the total tender amount awarded to vendors in each year."),
                    html.Li(
                        "Legend (VENDOR): Lists vendors contributing to the awarded amounts.")
                ]
            )
        ],
        style={'color': 'black'}
    )


def generate_general_word_cloud_message(unique_vendors_count, selected_item, is_cluster=False):
    if is_cluster:
        item_message = f"in the {selected_item} cluster"
    else:
        item_message = f"in the {selected_item} organization"

    return html.Div(
        children=[
            html.P(
                f"This word cloud visualizes the most frequently occurring words from tender descriptions"
                f" {item_message}, highlighting dominant themes. It offers insights into procurement focus areas and"
                f" commonly awarded vendor tasks. Generated from the tender descriptions of {unique_vendors_count} vendors"
                f" {item_message}, the word cloud emphasizes key themes and commonly awarded vendor names."
            ),
        ],
        style={'color': 'black'}
    )


def generate_topic_word_cloud_message(unique_vendors_count, selected_item, is_cluster=False):
    if is_cluster:
        item_message_one = f"in the {selected_item} cluster"
        item_message_two = f"within the {selected_item} cluster"
    else:
        item_message_one = f"in the {selected_item} organization"
        item_message_two = f"within the {selected_item} organization"

    return html.Div(
        children=[
            html.P(
                f"This BERTopic-based word cloud, generated from the tender descriptions of {unique_vendors_count} "
                f"vendors {item_message_one}, highlights key topics and frequently occurring words. It visualizes the"
                f" most prominent topics and terms reflecting the focus of procurement activities. Topic modeling"
                f" provides deeper insights into main themes and commonly awarded vendor names, offering a comprehensive"
                f" view of procurement priorities {item_message_two}."
            ),
        ],
        style={'color': 'black'}
    )
