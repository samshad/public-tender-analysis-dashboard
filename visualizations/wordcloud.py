import plotly.graph_objects as go
import base64
import io
from wordcloud import WordCloud


def create_word_cloud(text: str) -> go.Figure:
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    img = io.BytesIO()
    wordcloud.to_image().save(img, format='PNG')
    img.seek(0)
    encoded_image = base64.b64encode(img.getvalue()).decode()

    fig = go.Figure()
    fig.add_layout_image(
        dict(
            source="data:image/png;base64,{}".format(encoded_image),
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            sizex=1, sizey=1,
            xanchor="center", yanchor="middle"
        )
    )

    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig
