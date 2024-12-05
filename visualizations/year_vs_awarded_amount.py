import plotly.express as px
import pandas as pd

def create_year_vs_awarded_amount_bar_chart(tender_data: pd.DataFrame, content:str) -> px.bar:
    # Sort tender_data by 'VENDOR' case-insensitively
    tender_data = tender_data.sort_values(by='VENDOR', key=lambda col: col.str.lower())

    hover_data_map = {
        'ENTITY': 'Entity',
        'VENDOR': 'Vendor',
    }
    return px.bar(
        tender_data,
        x='YEAR',
        y='AWARDED_AMOUNT',
        color=content,
        hover_data=['AWARDED_AMOUNT', content],
        labels={'AWARDED_AMOUNT': 'Awarded Amount', 'YEAR': 'Year', content: hover_data_map[content]},
        text='AWARDED_AMOUNT'
    ).update_layout(
        xaxis_title="YEAR",
        yaxis_title="Awarded Amount",
        showlegend=True,
        bargap=0.1,
        margin=dict(l=80, r=80, t=80, b=80),
        xaxis_type='category'
    )
