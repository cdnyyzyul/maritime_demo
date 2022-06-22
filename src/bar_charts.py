'''
    Contains some functions related to the creation of the line chart.
'''
import plotly.express as px
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
                text="Select a region and a harbour to start.",
                showarrow=False,
                align="center",
            )
        ]
    )

    return fig



def get_region_figure(bar_data, region, year, trip_direction, harbour=""):
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

    total_counts = bar_data.Counts.sum()  # %
    fig = go.Figure()
    fig.add_trace(go.Bar(x=bar_data.Date, y=bar_data.Counts,
                         customdata = round(bar_data.Counts / total_counts * 100, 2)  # %
                         ))

    num_xticks = len(bar_data.Date.dt.month.unique())
    fig.update_xaxes(nticks=num_xticks)

    fig.update_layout(
        xaxis_tickformat='%b',
        xaxis_tickangle=0,
        yaxis_title="Number of voyages",
        xaxis_title=""
    )

    if trip_direction == 0:
        fig.update_layout(
            title=f"Monthly Departures in {region} {harbour} in {year}"
        )
        fig.update_traces(marker_color=THEME['line_bar_color_depart'])

    elif trip_direction == 1:
        fig.update_layout(
            title=f"Monthly Arrivals in {region} {harbour} in {year}"
        )
        fig.update_traces(marker_color=THEME['line_bar_color_arrival'])

    else:
        fig.update_layout(
            title=f"Monthly Voyages in {region} in {year}"
        )
        fig.update_traces(marker_color=THEME['line_bar_color_total'])

    fig.update_traces(
        hovertemplate = hover_template.get_singlebar_hover_template()
    )
    return fig


def get_harbour_figure_year(stack_bar_data, region, harbour):
    total_counts = stack_bar_data.Counts.sum()
    fig = px.bar(stack_bar_data, x=stack_bar_data.Date.dt.year, y="Counts",
                 color="Direction",
                 custom_data=["Direction", round(stack_bar_data.Counts/total_counts*100, 2)],
                 color_discrete_sequence=[THEME['line_bar_color_arrival'], THEME['line_bar_color_depart']])  # arrival, departure

    num_xticks = len(stack_bar_data.Date.dt.year.unique())
    fig.update_xaxes(nticks=num_xticks)
    fig.update_layout(xaxis=dict(tickmode='linear'),
                      yaxis_title="Number of voyages",
                      xaxis_title="",
                      title=f"Voyages in {region} in {harbour}"
                      )

    fig.update_traces(
        hovertemplate = hover_template.get_stackbar_hover_template()
    )

    return fig