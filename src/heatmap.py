
import plotly.express as px
import plotly.graph_objects as go
from template import THEME
import hover_template
import numpy as np


def get_figure(data, direction, total_voyage):
    '''
    Generates a heatmap from the given dataset.

    Args:
        data: The data to display
        direction: departure, arrival or both
        total_voyage: total number of voyage
    Returns:
        The figure to be displayed.
    '''

    # reverse the dataframe (shape: 9*11) before creating the heatmap. Plot uses reverse older.
    data = data[::-1]
    xticklabel = [i.year for i in data.columns]
    yticklabel = data.index


    fig = go.Figure(data=go.Heatmap(
        z=np.log10(data),
        x=xticklabel,
        y=yticklabel,
        colorbar_title="Voyage<br>(powers of 10)",
        customdata=round(data / total_voyage * 100, 2),
        text = data
    ))


    fig.update_layout(xaxis=dict(tickmode='linear'))

    if direction == 0:
        fig.update_traces(colorscale=THEME["departure_colorscales"])
        fig.update_layout(title_text="DEPARTURE BY REGION and YEAR")
    elif direction == 1:
        fig.update_traces(colorscale=THEME["arrival_colorscales"])
        fig.update_layout(title_text="ARRIVAL BY REGION and YEAR")
    else:
        fig.update_layout(title_text="VOYAGE BY REGION and YEAR")

    fig.update_traces(
        hovertemplate = hover_template.get_heatmap_hover_template()
    )

    return fig
