import plotly.express as px
import pandas as pd


def create_awarded_amount_vs_vendor_or_entity_bar_chart(
    awarded_amount: pd.DataFrame, data_count: int, x: str, y: str
) -> px.bar:
    """
    Creates a bar chart comparing awarded amounts against a specified variable.

    Parameters:
        awarded_amount (pd.DataFrame): DataFrame containing the data for plotting.
        x (str): Column name for the x-axis (e.g., 'VENDOR' or 'ENTITY').
        y (str): Column name for the y-axis (e.g., 'AWARDED_AMOUNT').

    Returns:
        px.bar: A Plotly bar chart.
    """
    # Validate input DataFrame
    if x not in awarded_amount.columns or y not in awarded_amount.columns:
        raise ValueError(f"Columns '{x}' and/or '{y}' not found in the DataFrame.")

    # Create the bar chart
    fig = px.bar(awarded_amount, x=x, y=y)

    # Update the axis titles dynamically
    fig.update_layout(
        xaxis_title="VENDOR", yaxis_title="TENDER AMOUNT", template="plotly"
    )

    return fig
