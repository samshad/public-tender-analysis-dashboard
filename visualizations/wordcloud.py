import plotly.graph_objects as go
import base64
import io
from wordcloud import WordCloud


def create_word_cloud(text: str) -> go.Figure:
    """
    Creates a word cloud from the given text and embeds it in a Plotly Figure.

    Parameters:
        text (str): The input text used to generate the word cloud.

    Returns:
        go.Figure: A Plotly figure containing the word cloud image.
    """
    # Validate input
    if not text.strip():
        raise ValueError("Input text must not be empty.")

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
        text
    )

    # Encode the image to base64
    img = io.BytesIO()
    wordcloud.to_image().save(img, format="PNG")
    img.seek(0)
    encoded_image = base64.b64encode(img.getvalue()).decode()

    # Create a Plotly figure and embed the image
    fig = go.Figure()
    fig.add_layout_image(
        dict(
            source=f"data:image/png;base64,{encoded_image}",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            sizex=1,
            sizey=1,
            xanchor="center",
            yanchor="middle",
        )
    )

    # Update layout to hide axes and set transparent background
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=30, b=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return fig
