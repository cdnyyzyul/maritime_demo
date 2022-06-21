'''
    Contains some functions related to the creation of the line chart.
'''
import plotly.graph_objects as go
import plotly.express as px
import hover_template
import numpy as np

from template import THEME


def get_empty_figure():
    '''
        Returns the figure to display when there is no data to show.

        The text to display is : 'No data to display. Select a cell
        in the heatmap for more information.

    '''

    # Construct the empty figure to display.

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
        Generates the dot chart using the given data.

    '''
    # Construct the required figure.

    fig_VRH = px.scatter(dotplot_data, x="Counts", y="Harbour",
                         title=f"{region} in {year}",
                         size=np.sqrt(dotplot_data.Counts),
                         )


    fig_VRH.update_traces(textposition='top right')
    fig_VRH.update_layout(xaxis=dict(showgrid=True, showline=False),
                          yaxis=dict(showgrid=False, showline=True),
                          height=800,
                          xaxis_title="Number of voyages",
                          )

    fig_VRH.update_traces(
        hovertemplate=hover_template.get_vesselport_hover_template()
    )


    return fig_VRH
