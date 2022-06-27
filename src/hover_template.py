'''
    templates for the tooltips.
'''

def get_heatmap_hover_template():
    '''
    template for the hover tooltips in the heatmap.
    the tooltip includes:
        Region name
        year
        Voyage: number of voyage
        %:  (number of voyage in a region in a year) / (total voyage)

    '''

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
    template for the hover tooltips of line charts.
    the tooltip includes:
        Date
        voyage: Number of voyage
        %: (number of voyage in a day) / (total voyages in a region/harbour in that year)
    '''

    hovertext = [
            "<span style='font-family:Open Sans'> <b>Date: </b>%{x}</span>",
            "<span style='font-family:Open Sans'> <b>Vogage: </b> %{y} (%{customdata}%)</span>",
            "<extra></extra>"
        ]

    template = "<br>".join(hovertext)

    return template


def get_singlebar_hover_template():
    '''
    template for hover tooltip of single bar charts.
    the tooltip includes:
        Month
        voyage: Number of voyage
        %: (number of voyage in a month) / (total voyages in a region/harbour in that year)
    '''

    hovertext = [
            "<span style='font-family:Open Sans'> <b>Month: </b>%{x}</span>",
            "<span style='font-family:Open Sans'> <b>Vogage: </b> %{y} (%{customdata}%)</span>",
            "<extra></extra>"
        ]

    template = "<br>".join(hovertext)

    return template


def get_stackbar_hover_template():
    '''
    template for hover tooltip of the stacked bar chart.
    the tooltip includes:

        Direction of the trip
        Year
        voyage: Number of voyage
        %:  (number of voyage in a region & harbour in a year) / (total of voyage)

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

    '''
    template for hover tooltip of the itinerary map.
    the tooltip includes:

        Region name
        Harbour name
        Event type: e.g. departure, arrival, CIP passage
        Direction of the trip
        Latitude of the event
        Longitude of the event

    '''

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
    '''
    template for hover tooltip of the dot plot.
    the tooltip includes:
        Harbour name
        voyage: Number of voyage
    '''

    hovertext = [
            "<span style='font-family:Open Sans'> <b>Harbour: </b>%{y}</span>",
            "<span style='font-family:Open Sans'> <b>Voyage: </b>%{x}</span>",
            "<extra></extra>"
        ]

    template = "<br>".join(hovertext)

    return template

