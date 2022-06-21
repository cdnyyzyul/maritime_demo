'''
    Contains the template to use in the data visualization.
'''
import plotly.graph_objects as go
import plotly.io as pio


THEME = {
    # 'background_color': '#ffffff',
    'font_family': 'Open Sans',
    # 'accent_font_family': 'Roboto Slab',
    'dark_color': '#2A2B2E',
    # 'pale_color': '#DFD9E2',
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

        The template sets the font color and
        font to the values defined above in
        the THEME dictionary, using the dark
        color.

        The plot background and paper background
        are the background color defined
        above in the THEME dictionary.

        Also, sets the hover label to have a
        background color and font size
        as defined for the label in the THEME dictionary.
        The hover label's font color is the same
        as the theme's overall font color. The hover mode
        is set to 'closest'.

        Sets the line chart's line color to the one
        designated in the THEME dictionary. Also sets
        the color scale to be used by the heatmap
        to the one in the THEME dictionary.

        Specifies the x-axis ticks are tilted 45
        degrees to the right.
    '''
    # Generate template described above

    pio.templates['new_theme'] = go.layout.Template(
        layout=go.Layout(
            title_font_size=22,
            # font_color=THEME["dark_color"],
            # font_family=THEME["font_family"],
            # plot_bgcolor=THEME["background_color"],
            # paper_bgcolor=THEME["background_color"],
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
        'plotly_white' theme and our custom theme.
    '''
    # Set default theme
    pio.templates.default = 'plotly_white+new_theme'
