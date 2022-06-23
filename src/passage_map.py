
import plotly.graph_objects as go
import plotly.express as px
import hover_template


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
                text="Invalid trip Id. Trip id is between 16 to 18 digits",
                showarrow=False,
                align="center",
            )
        ]
    )

    return fig



def get_passage_map(atrip):
    '''
    Generates a map showing the itinerary of atrip.

    Args:
        A dataframe of a trip.
    Returns:
        A map based on the input data.

    '''

    lats = atrip.Latitude
    longs = atrip.Longitude
    fig = px.scatter_mapbox(atrip, lat=lats, lon=longs,
                            hover_data=[atrip.Hardour, atrip.Region, atrip["Event Type"], atrip["Rank Number"]],
                            zoom=5
                            )
    fig.update_layout(mapbox_style="carto-positron"  # "stamen-toner",
                      )

    fig.update_traces(mode="lines+markers")

    fig.update_traces(
        hovertemplate=hover_template.get_map_hover_template()
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


    return fig
