import plotly.express as px
import pandas as pd


def create_tender_frequency_bar_chart(
    tender_frequency: pd.DataFrame,
    data_count: int,
    x: str,
    y: str
) -> px.bar:
    """
    Creates a bar chart to visualize the frequency of tenders by a specified variable.

    Parameters:
        tender_frequency (pd.DataFrame): DataFrame containing tender data.
        data_count (int): Number of top rows to include in the chart.
        x (str): Column name for the x-axis (e.g., 'VENDOR').
        y (str): Column name for the y-axis (e.g., 'FREQUENCY').

    Returns:
        px.bar: A Plotly bar chart.
    """
    # Validate input DataFrame
    if x not in tender_frequency.columns or y not in tender_frequency.columns:
        raise ValueError(f"Columns '{x}' and/or '{y}' not found in the DataFrame.")

    # Validate data_count
    if data_count <= 0 or data_count > len(tender_frequency):
        raise ValueError(f"data_count must be between 1 and {len(tender_frequency)}.")

    # Create the bar chart
    fig = px.bar(
        tender_frequency.head(data_count),
        x=x,
        y=y,
    )

    # Update layout dynamically based on x and y
    fig.update_layout(
        xaxis_title="VENDOR",
        yaxis_title="FREQUENCY OF TENDER",
        template="plotly"
    )

    return fig