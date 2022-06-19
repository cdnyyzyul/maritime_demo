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
            "<span style='font-family:Open Sans'> <b>Voyage: </b> %{z} (%{customdata}%)</span> ",
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
        Sets the template for the hover tooltips in the heatmap.

        Contains two labels, followed by their corresponding
        value, separated by a colon : date and trees planted.

        The labels are font 'Roboto Slab' and bold. The values
        are font 'Roboto' and regular weight.
    '''
    # Define and return the hover template

    hovertext = [
            "<span style='font-family:Open Sans'> <b>Direction: </b>%{customdata[0]}</span>",
            "<span style='font-family:Open Sans'> <b>Year: </b>%{x}</span>",
            "<span style='font-family:Open Sans'> <b>Vogage: </b> %{y} (%{customdata[1]}%)</span>",
            "<extra></extra>"
        ]

    template = "<br>".join(hovertext)

    return template