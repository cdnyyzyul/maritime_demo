
import plotly.graph_objects as go
import hover_template

from template import THEME


def get_empty_figure(page):
    '''
    Returns the figure when there is no data to show.

    '''
    text_info = {
        "region_page": "Select a cell in the heatmap<br>use the toggle to show daily or monthly voyages.",
        "harbour_page": "Click on a stacked bar<br>use the toggle to show daily or monthly voyages."
    }

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
                text=text_info[page],
                showarrow=False,
                align="center",
            )
        ]
    )

    return fig


def get_region_figure(line_data, region, year, trip_direction, harbour=""):
    '''
    Generates a line chart using the given data.

        Args:
            line_data: The data to display
            region: The selected region
            year: The selected year
            trip_direction: departure, arrival or both
            harbour: name of a harbour, default to empty string
        Returns:
            A figure to be displayed
    '''

    total_counts = line_data.Counts.sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=line_data.Date, y=line_data.Counts,
                             mode="lines",
                             customdata=round(line_data.Counts / total_counts * 100, 2)
                             ))

    num_xticks = len(line_data.Date.dt.month.unique())

    if line_data.shape[0] < 2:
        fig.update_traces(mode="lines+markers")
    else:
        fig.update_xaxes(nticks=num_xticks)

    fig.update_layout(
        xaxis_tickformat='%d %b',
        yaxis_title="Number of voyages",
        xaxis_title=""
    )

    if trip_direction == 0:
        fig.update_layout(
            title=f"Daily Departures in {region} {harbour} in {year}"
        )
        fig.update_traces(line=dict(color=THEME['line_bar_color_depart']),
                          marker_color=THEME['line_bar_color_depart'])

    elif trip_direction == 1:
        fig.update_layout(
            title=f"Daily Arrivals in {region} {harbour} in {year}"
        )
        fig.update_traces(line=dict(color=THEME['line_bar_color_arrival']),
                          marker_color=THEME['line_bar_color_arrival'])

    else:
        fig.update_layout(
            title=f"Daily Voyages in {region} in {year}"
        )
        fig.update_traces(line=dict(color=THEME['line_bar_color_total']),
                          marker_color=THEME['line_bar_color_total'])

    fig.update_traces(
        hovertemplate = hover_template.get_linechart_hover_template()
    )
    return fig
