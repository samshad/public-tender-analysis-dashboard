import plotly.express as px
import pandas as pd

def create_year_vs_awarded_amount_bar_chart(tender_data: pd.DataFrame, content:str) -> px.bar:
    hover_data_map = {
        'ENTITY': 'Entity',
        'VENDOR': 'Vendor',
    }

    # Extract unique years and sort them
    unique_years = sorted(tender_data['YEAR'].unique())

    return px.bar(
        tender_data,
        x='YEAR',
        y='AWARDED_AMOUNT',
        color=content,
        custom_data=['TENDER_ID'],
        hover_data=['AWARDED_AMOUNT', content],
        labels={'AWARDED_AMOUNT': 'Awarded Amount', 'YEAR': 'Year', content: hover_data_map[content]},
        text='AWARDED_AMOUNT'
    ).update_layout(
        xaxis_title="YEAR",
        yaxis_title="Awarded Amount",
        showlegend=True,
        bargap=0.1,
        margin=dict(l=80, r=80, t=80, b=80),
        xaxis_type='category',
        xaxis=dict(categoryorder="array", categoryarray=unique_years)
    )
