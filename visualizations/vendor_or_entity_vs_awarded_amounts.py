import plotly.express as px
import pandas as pd

def create_awarded_amount_vs_vendor_or_entity_bar_chart(awarded_amount: pd.DataFrame, data_count: int, x: str, y: str) -> px.bar:
    fig = px.bar(
        awarded_amount,
        x=x,
        y=y
    )

    # Update the axis titles
    fig.update_layout(
        xaxis_title="VENDOR",
        yaxis_title="TENDER AMOUNT",
        template="plotly"
    )

    return fig
