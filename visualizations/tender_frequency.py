import plotly.express as px
import pandas as pd

def create_tender_frequency_bar_chart(tender_frequency: pd.DataFrame, data_count: int, x: str, y: str) -> px.bar:
    fig = px.bar(
        tender_frequency.head(data_count),
        x=x,
        y=y,
    )

    # Update the axis titles
    fig.update_layout(
        xaxis_title="VENDOR",
        yaxis_title="FREQUENCY OF TENDER",
        template="plotly"
    )

    return fig