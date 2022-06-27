
import plotly.express as px
import plotly.graph_objects as go
import hover_template

from template import THEME


def get_empty_figure():
    '''
    Returns the figure when there is no data to show.

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
                text="Select a region and a harbour to start.",
                showarrow=False,
                align="center",
            )
        ]
    )

    return fig



def get_region_figure(bar_data, region, year, trip_direction, harbour=""):
    '''
    Generates a bar chart using the given data.

        Args:
            bar_data: The data to display
            region: The selected region
            year: The selected year
            trip_direction: departure, arrival or both
            harbour: name of a harbour, default to empty string
        Returns:
            A figure to be displayed
    '''

    total_counts = bar_data.Counts.sum()  #  to calculate %
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
    '''
    Generates a stacked bar chart using the given data.

        Args:
            stack_bar_data: The data to display
            region: The selected region
            harbour: name of a harbour, default to empty string
        Returns:
            A figure to be displayed
    '''

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