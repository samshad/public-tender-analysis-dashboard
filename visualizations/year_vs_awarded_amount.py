import plotly.express as px
import pandas as pd


def create_year_vs_awarded_amount_bar_chart(
    tender_data: pd.DataFrame, content: str
) -> px.bar:
    """
    Creates a bar chart of Year vs. Awarded Amount with color-coded categories.

    Parameters:
        tender_data (pd.DataFrame): The tender dataset containing 'YEAR', 'AWARDED_AMOUNT', and content columns.
        content (str): The column name used for color-coding (e.g., 'ENTITY' or 'VENDOR').

    Returns:
        px.Figure: A Plotly bar chart.
    """
    # Map for hover data labels
    hover_data_map = {
        "ENTITY": "Entity",
        "VENDOR": "Vendor",
    }

    # Validate the provided 'content' column
    if content not in hover_data_map:
        raise ValueError(
            f"Invalid content: '{content}'. Expected one of {list(hover_data_map.keys())}."
        )

    # Extract unique years and sort them
    if "YEAR" not in tender_data.columns:
        raise ValueError("The provided DataFrame does not contain a 'YEAR' column.")
    unique_years = sorted(tender_data["YEAR"].unique())

    # Create the bar chart
    fig = px.bar(
        tender_data,
        x="YEAR",
        y="AWARDED_AMOUNT",
        color=content,
        custom_data=["TENDER_ID"],
        hover_data=["AWARDED_AMOUNT", content],
        labels={
            "AWARDED_AMOUNT": "Awarded Amount",
            "YEAR": "Year",
            content: hover_data_map[content],
        },
        text="AWARDED_AMOUNT",
    )

    # Update layout for improved appearance
    fig.update_layout(
        xaxis_title="YEAR",
        yaxis_title="Awarded Amount",
        showlegend=True,
        bargap=0.1,
        margin=dict(l=80, r=80, t=80, b=80),
        xaxis_type="category",
        xaxis=dict(categoryorder="array", categoryarray=unique_years),
    )

    return fig
