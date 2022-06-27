
import plotly.graph_objects as go
import plotly.express as px
import hover_template
import numpy as np


def get_empty_figure():
    '''
    Returns the figure to display when there is no data to show.
    '''

    fig = go.Figure()
    fig.update_layout(
        showlegend=False,
        xaxis={"visible": False},
        yaxis={"visible": False},
        dragmode=False,
        annotations=[
            dict(
                xref="paper",
                yref="paper",
                text="Select a cell in the heatmap to show voyages in harbours.",
                showarrow=False,
                align="center",
            )
        ]
    )

    return fig



def get_vesselport_figure(dotplot_data, region, year):
    '''
    Generates the dot plot using the given data.

    Args:
        A dataframe and necessary data to generate a dot plot.
        region name
        year
    Returns:
        A figure based on input data.

    '''

    fig_VRH = px.scatter(dotplot_data, x="Counts", y="Harbour",
                         title=f"{region} in {year}",
                         size=np.sqrt(dotplot_data.Counts),
                         )


    fig_VRH.update_traces(textposition='top right')
    fig_VRH.update_layout(xaxis=dict(showgrid=True, showline=False),
                          yaxis=dict(showgrid=False, showline=True),
                          height=700,
                          xaxis_title="Number of voyages",
                          xaxis_tickangle=0
                          )

    fig_VRH.update_traces(
        hovertemplate=hover_template.get_vesselport_hover_template()
    )


    return fig_VRH
