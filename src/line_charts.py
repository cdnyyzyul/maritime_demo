'''
    Contains some functions related to the creation of the line chart.
'''
import plotly.graph_objects as go
import hover_template

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
                text="Select a cell in the heatmap to show daily voyages.",
                showarrow=False,
                align="center",
            )
        ]
    )

    return fig


def add_rectangle_shape(fig):
    '''
        Adds a rectangle to the figure displayed
        behind the informational text. The color
        is the 'pale_color' in the THEME dictionary.

        The rectangle's width takes up the entire
        paper of the figure. The height goes from
        0.25% to 0.75% the height of the figure.
    '''
    # Draw the rectangle

    fig.update_layout(
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                #fillcolor=THEME["pale_color"],
                x0=0, y0=0.25, x1=1, y1=0.75,
                line=dict(width=0)
            )
        ]
    )
    return None


def get_region_figure(line_data, region, year, trip_direction, harbour=""):
    '''
        Generates the line chart using the given data.

        The ticks must show the zero-padded day and
        abbreviated month. The y-axis title should be 'Trees'
        and the title should indicated the displayed
        neighborhood and year.

        In the case that there is only one data point,
        the trace should be displayed as a single
        point instead of a line.

        Args:
            line_data: The data to display in the
            line chart
            region: The selected region
            year: The selected year
        Returns:
            The figure to be displayed
    '''
    # Construct the required figure. Don't forget to include the hover template

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
