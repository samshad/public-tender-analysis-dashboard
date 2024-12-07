import plotly.graph_objects as go
import pandas as pd


def create_topic_time_visualization(
        topic_counts: pd.DataFrame,
        topic_keywords: dict,
        selected_item: str,
        is_cluster: bool = False
) -> tuple[go.Figure, str]:
    """
    Creates a line chart to visualize the evolution of topics over time.

    Parameters:
        topic_counts (pd.DataFrame): DataFrame where columns are topics and rows are years,
                                     containing counts of documents per topic per year.
        topic_keywords (dict): Dictionary mapping topics to their associated keywords.
        selected_item (str): The cluster or organization being analyzed.
        is_cluster (bool): If True, indicates the data represents clusters; otherwise, organizations.

    Returns:
        tuple[go.Figure, str]: A Plotly Figure of the topic visualization and a descriptive text.
    """
    # Validate input DataFrame
    if topic_counts.empty or not isinstance(topic_keywords, dict):
        raise ValueError(
            "Invalid input: Ensure 'topic_counts' is a non-empty DataFrame and 'topic_keywords' is a dictionary.")

    fig = go.Figure()
    for topic in topic_counts.columns:
        # Validate that keywords exist for the topic
        keywords = topic_keywords.get(topic, "No keywords available")

        fig.add_trace(go.Scatter(
            x=topic_counts.index,
            y=topic_counts[topic],
            mode='lines+markers',
            name=f'Topic {topic}',
            hovertemplate=(f"Topic {topic}<br>"
                           f"Keywords: {keywords}<br>"
                           f"Year: %{{x}}<br>"
                           f"Count: %{{y}}<br>"
                           f"<extra></extra>")
        ))

    # Update layout
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Documents",
        hovermode="x unified",
        template="plotly",
        title_text="Topic Evolution Over Time",
        title_x=0.5
    )

    # Generate description text
    cluster_text = f"within the {selected_item} cluster" if is_cluster else f"within the {selected_item} organization"
    topic_description = (
        f"This visualization tracks the evolution of topics over time {cluster_text}. "
        f"The line chart shows how frequently each topic appears in tender descriptions across different years, "
        f"offering insights into trends and shifts in tender types. By analyzing these trends, we can identify periods "
        f"when certain topics gained or lost prominence, indicating emerging priorities, technological advancements, "
        f"or shifts in procurement focus."
    )

    return fig, topic_description