import plotly.graph_objects as go

def create_topic_time_visualization(topic_counts, topic_keywords, selected_item, is_cluster=False):
    fig = go.Figure()
    for topic in topic_counts.columns:
        fig.add_trace(go.Scatter(
            x=topic_counts.index,
            y=topic_counts[topic],
            mode='lines+markers',
            name=f'Topic {topic}',
            hovertemplate=(
                f"Topic {topic}<br>" 
                f"Keywords: {topic_keywords[topic]}<br>" 
                f"Year: %{{x}}<br>"  
                f"Count: %{{y}}<br>" 
                f"<extra></extra>"
            )
        ))

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Documents",
        hovermode="x unified",
        template="plotly"
    )

    cluster_text = f"within the {selected_item} cluster" if is_cluster else f"within the {selected_item} organization"
    topic_description = (
        f"This visualization tracks the evolution of topics over time {cluster_text}."
        f" The line chart shows how frequently each topic appears in tender descriptions across different years,"
        f" offering insights into trends and shifts in tender types. By analyzing these trends, we can identify periods"
        f" when certain topics gained or lost prominence, indicating emerging priorities, technological advancements,"
        f" or shifts in procurement focus.")

    return fig, topic_description