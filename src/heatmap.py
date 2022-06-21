'''
    Contains some functions related to the creation of the heatmap.
'''
import plotly.express as px
import plotly.graph_objects as go
from template import THEME
import hover_template
import numpy as np


def get_figure(data, direction, total_voyage):
    '''
        Generates the heatmap from the given dataset.

        Make sure to set the title of the color bar to 'Trees'
        and to display each year as an x-tick.

        Args:
            data: The data to display
        Returns:
            The figure to be displayed.
    '''

    # Create the heatmap.
    data = data[::-1]
    xticklabel = [i.year for i in data.columns]
    yticklabel = data.index

    # fig = px.imshow(data,
    #                 labels=dict(x="", y="", color="Voyage"),
    #                 x=xticklabel,
    #                 y=yticklabel
    #                 )
    fig = go.Figure(data=go.Heatmap(
        z=np.log10(data),
        x=xticklabel,
        y=yticklabel,
        colorbar_title="Voyage",
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
