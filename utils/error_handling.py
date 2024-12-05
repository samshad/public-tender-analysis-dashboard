import plotly.graph_objects as go

def return_empty_plot():
    return go.Figure().update_layout(
        annotations=[{
            'text': "Not enough tender descriptions to visualize topics over time. Please select more data.",
            'xref': 'paper', 'yref': 'paper',
            'x': 0.5, 'y': 0.5,
            'xanchor': 'center', 'yanchor': 'middle',
            'showarrow': False,
            'font': {'size': 16, 'color': 'red'}
        }]
    )