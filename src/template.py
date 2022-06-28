
import plotly.graph_objects as go
import plotly.io as pio


THEME = {
    'font_family': 'Open Sans',
    'dark_color': '#2A2B2E',
    'line_chart_color': '#97939A',
    'line_bar_color_depart':'#0077DD',
    'line_bar_color_arrival': '#8F329F',         # '#5b5b5b', grey was not recommended. change to purple.
    'line_bar_color_total':'#008000',
    'departure_colorscales':"blues",
    'arrival_colorscales':"purples",   # change from grays.
    'label_font_size': 14,
    'label_background_color': '#ffffff',
    'colorscale': 'greens'
}


def create_custom_theme():
    '''
        Adds a new layout template to pio's templates.

        The template sets the paper background and the default colour for plot to the colour of total trips.
        sets the hover label, background color and font size.
        Specifies the x-axis ticks are tilted 45 degrees to the right.
    '''

    pio.templates['new_theme'] = go.layout.Template(
        layout=go.Layout(
            title_font_size=18,

            xaxis=dict(
                tickangle=-45
            ),
            hoverlabel=dict(
                bgcolor=THEME["label_background_color"],
                font_size=THEME["label_font_size"],
                font_color=THEME["dark_color"],
                font_family=THEME["font_family"]
            ),
            hovermode = "closest"
        ),

        data_heatmap=[go.Heatmap(colorscale=THEME["colorscale"])],

        data_scatter =[go.Scatter(mode = "lines+markers", marker_color=THEME['line_chart_color'],
                                  line=dict(color = THEME['line_chart_color'],
                                           dash = "solid")
                                  )]
    )
    pio.templates['new_theme'].layout.colorscale.sequential = THEME["colorscale"]

def set_default_theme():
    '''
        Sets the default theme to be a combination of the
        'plotly_white' theme and the custom theme.
    '''

    pio.templates.default = 'plotly_white+new_theme'
