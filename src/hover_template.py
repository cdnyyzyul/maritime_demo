'''
    Provides the templates for the tooltips.
'''


def get_heatmap_hover_template():
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains three labels, followed by their corresponding
        value, separated by a colon : neighborhood, year and
        trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    # Define and return the hover template

    hovertext = [
            "<span style='font-family:Open Sans; font-size:16px'> <b>Region: </b>%{y}</span>",
            "<span style='font-family:Open Sans'> <b>Year: </b> %{x}</span>",
            "<span style='font-family:Open Sans'> <b>Voyage: </b> %{text} (%{customdata}%)</span> ",
            "<extra></extra>"
        ]

    template = "<br>".join(hovertext)

    return template


def get_linechart_hover_template():
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains two labels, followed by their corresponding
        value, separated by a colon : date and trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    # Define and return the hover template

    hovertext = [
            "<span style='font-family:Open Sans'> <b>Date: </b>%{x}</span>",
            "<span style='font-family:Open Sans'> <b>Vogage: </b> %{y} (%{customdata}%)</span>",
            "<extra></extra>"
        ]

    template = "<br>".join(hovertext)

    return template


def get_singlebar_hover_template():
    '''
        Sets the template for the hover tooltips in the heatmap.

        Contains two labels, followed by their corresponding
        value, separated by a colon : date and trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    # Define and return the hover template

    hovertext = [
            "<span style='font-family:Open Sans'> <b>Month: </b>%{x}</span>",
            "<span style='font-family:Open Sans'> <b>Vogage: </b> %{y} (%{customdata}%)</span>",
            "<extra></extra>"
        ]

    template = "<br>".join(hovertext)

    return template


def get_stackbar_hover_template():
    '''
    template for the hover tooltips.

    Direction of the trip
    Number of trips
    % of total voyages in a region/harbour

    '''

    hovertext = [
            "<span style='font-family:Open Sans'> <b>Direction: </b>%{customdata[0]}</span>",
            "<span style='font-family:Open Sans'> <b>Year: </b>%{x}</span>",
            "<span style='font-family:Open Sans'> <b>Vogage: </b> %{y} (%{customdata[1]}%)</span>",
            "<extra></extra>"
        ]

    template = "<br>".join(hovertext)

    return template


def get_map_hover_template():

    # Define and return the hover template

    hovertext = [
            "<span style='font-family:Open Sans'> <b>Region: </b>%{customdata[1]}</span>",
            "<span style='font-family:Open Sans'> <b>Harbour: </b>%{customdata[0]}</span>",
            "<span style='font-family:Open Sans'> <b>Event Type: </b>%{customdata[2]}</span>",
            "<span style='font-family:Open Sans'> <b>Latitude: </b> %{lat}</span>",
            "<span style='font-family:Open Sans'> <b>Longitude: </b> %{lon}</span>",
            "<extra></extra>"
        ]

    template = "<br>".join(hovertext)

    return template


def get_vesselport_hover_template():

    # Define and return the hover template

    hovertext = [
            "<span style='font-family:Open Sans'> <b>Harbour: </b>%{y}</span>",
            "<span style='font-family:Open Sans'> <b>Voyage: </b>%{x}</span>",
            "<extra></extra>"
        ]

    template = "<br>".join(hovertext)

    return template

