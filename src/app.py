
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''

import json
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import template
import preprocess
import heatmap, line_charts, bar_charts, hover_template, dot_charts, passage_map
#
#
# Read: When data is local, read and process original trip file.
# trips_filename = "./assets/data/TRIP_NEW.csv"
# detail_filename = "./assets/data/TRIP_DETAIL_NEW.csv"
# or read from a smaller file (get rid of the columns we do not use)
# trips_filename = "./assets/data/trips_slim0.csv"
# detail_filename = "./assets/data/detail_sample.csv"  # testing upload

# trips_df_heat = pd.read_csv(trips_filename)
# detail_df = pd.read_csv(detail_filename)
# end Read data local.


# for web-hosting:
trips_df_heat = pd.read_csv("https://inf8808-vis-test.s3.amazonaws.com/web-hosting/trips_slim.csv")
detail_df = pd.read_csv("https://inf8808-vis-test.s3.amazonaws.com/web-hosting/detail_sample.csv")
# end for web hosting.

trips_df_heat = preprocess.convert_dates(trips_df_heat)
trips_df_heat = preprocess.filter_years(trips_df_heat, 2011, 2021)  # to be used in region, harbour, vessel.

#
# debug start
# yearly_df = preprocess.summarize_yearly_counts(trips_df_heat, 0) # 0 means Departure trip, comes from radio button
# data = preprocess.restructure_df(yearly_df)

# eg_region = "St. Lawrence Seaway Region"
# eg_harbour = "Lac St-Louis (area)"
# year = 2016
# line_data = preprocess.get_depart_by_harbour(trips_df_heat, eg_region, eg_harbour)
# line_data = preprocess.prepare_day_month_data_by_harbour(line_data, year, "daily")
# debug end

# summary panel
total_voyage0 = trips_df_heat.shape[0]
total_voyage = "{:,}".format(total_voyage0)
international_trips = preprocess.get_international_trips(trips_df_heat)
most_used_vessel = trips_df_heat[["Vessel Type", "Id"]].groupby("Vessel Type"
                                                                ).count().sort_values(by="Id", ascending=False).index[0]
trip_duration = preprocess.get_trip_duration(trips_df_heat, total_voyage0)

# region, harbour, vessel
regions_sorted = sorted(trips_df_heat["Departure Region"].unique())
vessel_type_sorted = sorted(trips_df_heat["Vessel Type"].unique())


template.create_custom_theme()
template.set_default_theme()


radio_trip_direction = dcc.RadioItems(
    id="trip_direction",
    options=[
        dict(label="Departure", value=0),
        dict(label="Arrival", value=1),
        dict(label="Both", value=2)
    ],
    value=0,
    inline=True,
    style={"display":"flex",
           "place-content":"space-around",
           "width": "30%"}
)

feature_ops = dbc.RadioItems(
    id="feature_ops",
    className="radio",
    options=[
        dict(label="REGION", value=0),
        dict(label="HARBOUR", value=1),
        dict(label="VESSEL", value=2),
        dict(label="VOYAGE", value=3),
    ],
    value=0,
    inline=True,
)




# ----------------- app  ------------------------
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.title = 'PROJECT | INF8808'


app.layout = html.Div([
    html.Div([
        html.H1('Maritime Traffic in Canada'),
    ]),

    # dcc.Store stores the intermediate value
    dcc.Store(id='intermediate-value-region-trip-direction'),

# panel summary
    html.Div([
        html.Div([
            html.H2(
                "Summary statistic of maritime traffic in Canada from 2011 to 2021.",
                style={
                       "margin-left": "4%" },
            ),
            html.Div([
                    html.Div([
                            html.H4(
                                "VOYAGE (Total Number)",
                                style={
                                    "font-weight": "normal"
                                },
                            ),
                            html.H3(
                                html.P(total_voyage),
                                id="trip_total"
                            ),
                        ],
                        className="box_summary",
                    ),
                    html.Div([
                            html.H4(
                                "International",
                                style={
                                    "font-weight": "normal"
                                },
                            ),
                            html.H3(
                                html.P(international_trips),
                                id="trip_international"
                            ),
                        ],
                        className="box_summary",
                    ),
                    html.Div([
                            html.H4(
                                "DURATION (hours/voyage)",
                                style={
                                    "font-weight": "normal"
                                },
                            ),
                            html.H3(
                                html.P(trip_duration),
                                id="trip_duration"
                            ),
                        ],
                        className="box_summary",
                    ),
                    html.Div([
                        html.H4(
                            "Most used Vessel Type",
                            style={
                                "font-weight": "normal"
                            },
                        ),
                        html.H3(
                            html.P(most_used_vessel),
                            id="vessel_king"
                        ),
                    ],
                        className="box_summary",
                    ),

                ],
                style={"display": "flex"},
            ),
        ],
            className="box",
            style={
                "margin": "0px",
                "padding-top": "0px",
                "padding-bottom": "0px",
                "heigth": "100%",
                "width": "100%"},
        ),
    ]),

# feature / page selection buttons

    html.Div([
        html.Div([
            feature_ops,
            ],
            className="box",
            style={
                "margin": "2px",
                "padding-top": "2px",
                "padding-bottom": "2px",
            },
        ),

        html.Div(id="output"),  # callback return html.Div()

    ])
]
)
# -------------------------------callback ----------------------

# page selection
@app.callback(
    Output(component_id='output', component_property='children'),
    [Input('feature_ops', 'value')],
)
def update_page(filter_chosen):
 # region page
    if filter_chosen == 0:
        return html.Div([

            html.Div([
                radio_trip_direction,

                daq.ToggleSwitch(
                    id='region-toggle',
                    label='Daily or Monthly',
                    labelPosition='bottom',
                    color="#8BC8FF",
                    value=False,
                ),
            ],
                className='row',
            ),

            html.Div([
            html.Div([
                dcc.Graph(
                    id='heatmap_region',
                    figure={},
                    className='graph',
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    )
                ),
            ],
                className="box",
                style={
                    "margin": "2px",
                    "padding-top": "2px",
                    "padding-bottom": "2px",
                    "width": "100%"
                },
            ),

            html.Div([
                dcc.Graph(
                    id='line_region',
                    className='graph',
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        doubleClick=False,
                        displayModeBar=False
                    )
                )
            ],
                className="box",
                style={
                    "margin": "2px",
                    "padding-top": "2px",
                    "padding-bottom": "2px",
                    "width": "100%"
                },
            ),
            ],
                className='row'
            )
        ])


    # harbour page
    elif filter_chosen == 1:
        return html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                                html.Label("Select a Region",
                                   style={"padding-left": "20px"},
                                   ),
                                html.Div([
                                    dcc.Dropdown(id='region_selector', multi=False,
                                                 options=[{'label': x, 'value': x} for x in regions_sorted],
                                                 value="Pacific Region",
                                                 searchable=True,
                                                 clearable=True,
                                                 style={'width': "98%"}, ),
                                ]),
                            ],
                            className='box',
                            style={"width": "40%",
                                   "box-shadow": "0px 0px 0px #F9F9F8"},
                        ),
                        html.Div([
                                html.Label('Select a harbour',
                                       style={"padding-left": "20px"},
                                       ),
                                html.Div([
                                    dcc.Dropdown(
                                                 id='harbour_selector', multi=False,
                                                 searchable=True,
                                                 placeholder='Select a Region, then a Harbour...',
                                                 clearable=True,
                                                 style={'width': "98%"}, ),
                                ]),
                            ],
                            className='box',
                            style={"width": "40%",
                                   "box-shadow": "0px 0px 0px #F9F9F8"},
                        ),
                        html.Div([
                            daq.ToggleSwitch(
                                id='harbour-toggle',
                                label='Daily or Monthly',
                                labelPosition='bottom',
                                color="#8BC8FF",
                                value=False,
                            ),
                        ],
                           className='box',
                            style={"box-shadow": "0px 0px 0px #F9F9F8"}
                        ),
                    ],
                        className="row",
                        style={
                            "padding-top": "8px",
                            "padding-bottom": "8px",},
                    ),
                ]),

            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='bar_harbour_year',
                            className='graph',
                            figure={},
                            config=dict(
                                scrollZoom=False,
                                showTips=False,
                                showAxisDragHandles=False,
                                doubleClick=False,
                                displayModeBar=False
                            )
                        ),
                    ])
                ],
                    className="box",
                    style={
                        "margin": "2px",
                        "padding-top": "2px",
                        "padding-bottom": "2px",
                         "width": "100%",
                           },
                ),

                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='line_harbour',
                            className='graph',
                            figure={},
                            config=dict(
                                scrollZoom=False,
                                showTips=False,
                                showAxisDragHandles=False,
                                doubleClick=False,
                                displayModeBar=False
                            )
                        ),
                    ])
                ],
                    className="box",
                    style={
                        "margin": "2px",
                        "padding-top": "2px",
                        "padding-bottom": "2px",
                         "width": "100%",
                           },
                ),
            ],
                className='row'
            ),
        ])


    # vessel page
    elif filter_chosen == 2:
        return html.Div([
                html.Div([
                    html.Div([
                        html.Br(),
                        html.Div([
                            html.Div([
                                "Select a Vessel Type",
                                dcc.Dropdown(id='vessel_selector', multi=False,
                                             options=[{'label': x, 'value': x} for x in vessel_type_sorted],
                                             value="Special Purpose",
                                             searchable=True,
                                             clearable=False,
                                             style={'width': "60%"}, ),
                            ]),
                            html.Br(),
                            html.Br(),
                            html.Div([
                                dcc.Graph(
                                    id='heatmap_vessel',
                                    className='graph',
                                     figure={},
                                    config=dict(
                                        scrollZoom=False,
                                        showTips=False,
                                        showAxisDragHandles=False,
                                        doubleClick=False,
                                        displayModeBar=False
                                    )
                                ),
                            ]),

                        ]),
                ],
                    className="box",
                    style={
                        "margin": "2px",
                        "padding-top": "2px",
                        "padding-bottom": "2px",
                        "heigth": "100%",
                        "width": "65%"},
                    ),

                    html.Div([
                        html.Div([
                            dcc.Graph(
                                id='dot_vessel',
                                className='graph',
                                figure={},
                                config=dict(
                                    scrollZoom=False,
                                    showTips=False,
                                    showAxisDragHandles=False,
                                    doubleClick=False,
                                    displayModeBar=False
                                )
                            ),
                        ]),
                    ],
                        className="box",
                        style={
                            "margin": "2px",
                            'background-color': '#ffffff',
                            "heigth": "100%",
                            "width": "34%",
                        },
                    )
                ],
                    className="row",
                ),
        ])


    # voyage page
    else:
        return html.Div([
            html.Div([
                html.Div([
                    html.Br(),
                    html.Label(
                        "Fill in a trip Id. e.g., 2079000000818245, empty map inidcates invalid Id. "
                    ),

                    html.Div([
                        html.Div([
                            dcc.Input(id="trip_input", type="number",
                                      value=2079000000818245,
                                      placeholder="digits",
                                      debounce=True),
                        ]),
                        html.Br(),
                        html.Br(),
                        html.Div([
                            dcc.Graph(
                                id='trip_passage',
                                className='graph',
                                figure={},
                                config=dict(
                                    scrollZoom=False,
                                    showTips=False,
                                    showAxisDragHandles=False,
                                    doubleClick=False,
                                    displayModeBar=False
                                )
                            ),
                        ],
                            className="box",
                            style = {
                                "margin": "4px",
                                "padding-top": "2px",
                                "padding-bottom": "2px",
                                "heigth": "100%",
                                "width": "96%"},
                        ),

                    ]),
                ],
                    className="box",
                    style={
                        "margin": "4px",
                        "padding-top": "2px",
                        "padding-bottom": "2px",
                        "heigth": "100%",
                        "width": "100%"},
                ),
            ],
            ),
            # we have an extra Div layer in case new graph box is needed.
        ])


# region page features: show heatmap
@app.callback(
    Output("heatmap_region", "figure"),
    [Input("trip_direction", "value")],
)
def update_region_heat(direction_chosen):
    '''
        Display a heatmap based on radio button value.

        Args:
            The radio button value indicating trip directions. default to 0,
            means departure.
        Returns:
            The necessary output values to update the heatmap.

    '''

    yearly_df = preprocess.summarize_yearly_counts(trips_df_heat, direction_chosen)  # 0 means Departure
    data = preprocess.restructure_df(yearly_df)


    region_heat_fig = heatmap.get_figure(data, direction_chosen, total_voyage0)

    return region_heat_fig


# region page features: show line or bar
@app.callback(
    Output('line_region', 'figure'),
    [Input('heatmap_region', 'clickData'),
     Input("trip_direction", "value"),
     Input('region-toggle', 'value')]
)
def region_heatmap_clicked(click_data, stored_direction, toggle_value):
    '''
        When a cell in the heatmap is clicked, updates the
        line or bar chart shows the data for the corresponding
        region & year. If there is no data to show,
        displays a message. The toggle selects line or bar charts.

        Args:
            The necessary inputs to update the line or bar chart.
        Returns:
            The necessary output values to update the line or bar
            chart.
    '''
    if click_data is None or click_data['points'][0]['z'] == None:
        line_fig_empty = line_charts.get_empty_figure("region_page")

        return line_fig_empty

    region = click_data['points'][0]['y']
    year = click_data['points'][0]['x']

    if not toggle_value:
        # daily trip line chart
        line_data = preprocess.get_data_by_freq(
            trips_df_heat,
            region,
            year,
            stored_direction,
            "daily"
        )

        my_fig = line_charts.get_region_figure(line_data, region, year, stored_direction)

    else:
        # monthly trip bar chart
        bar_data = preprocess.get_data_by_freq(
            trips_df_heat,
            region,
            year,
            stored_direction,
            "monthly"
        )

        my_fig = bar_charts.get_region_figure(bar_data, region, year, stored_direction)

    return my_fig


# harbour page features: chained dropdown
@app.callback(
    Output('harbour_selector', 'options'),
    [Input('region_selector', 'value')],
)
def set_harbour_options(region_chosen):
    '''
        Dropdowns to select Region and Harbour. The harbour download is populated based on
        the Region value.

        Args:
            The dropdown indicates a Region, defaults to "Pacific Region".
        Returns:
            The necessary output values to update the harbour dropdown.
    '''
    regions_harbours = preprocess.all_region_harbour(trips_df_heat)
    harbours = preprocess.get_harbours_by_region(regions_harbours, region_chosen)

    return [{'label': x, 'value': x} for x in harbours]


# harbour page features: stack bar
@app.callback(
    Output('bar_harbour_year', 'figure'),
    [Input('region_selector', 'value'),
     Input('harbour_selector', 'value')]
)
def add_stack_bar(region, harbour):
    '''
        Display a stacked bar based on the input value from Region and Harbour dropdowns.

        Args:
            The dropdowns indicate a Region and a harbour in the region.
        Returns:
            The necessary output values to update the stacked bar.
    '''

    ctx = dash.callback_context
    my_trigger = ctx.triggered

    if my_trigger[0]['prop_id'] == "region_selector.value":
        harbour= None

    if not region or not harbour:
        bar_fig_empty = bar_charts.get_empty_figure()

        return bar_fig_empty


    stack_bar_data_depart = preprocess.get_depart_by_harbour(trips_df_heat, region, harbour)
    stack_bar_data_arrive = preprocess.get_arrive_by_harbour(trips_df_heat, region, harbour)
    stack_bar_data = preprocess.prepare_data_by_harbour(stack_bar_data_depart,
                                                        stack_bar_data_arrive)

    if stack_bar_data.shape[0] < 1:
        bar_fig_empty = bar_charts.get_empty_figure()
        return bar_fig_empty
    else:
        stack_bar_fig = bar_charts.get_harbour_figure_year(stack_bar_data, region, harbour)

    return stack_bar_fig


# harbour page features: click stack bar to show line daily or bar monthly
@app.callback(
    Output('line_harbour', 'figure'),
    [Input('bar_harbour_year', 'clickData'),
     Input('region_selector', 'value'),
     Input('harbour_selector', 'value'),
     Input('harbour-toggle', 'value')]
)
def region_stack_bar_clicked(click_data, region_chosen, harbour_chosen, toggle_value):
    '''
        When a section of a stack bar is clicked, updates the
        line or bar chart to show the data for the corresponding
        harbour & year. If there is no data to show, displays a message.
        The toggle selects line or bar charts.

        Args:
            The necessary inputs to update the line or bar chart.
        Returns:
            The necessary output values to update the line or bar
            chart.
    '''

    ctx = dash.callback_context
    my_trigger = ctx.triggered
  #  print(my_trigger)

    if my_trigger[0]['prop_id'] == "region_selector.value" or my_trigger[0]['prop_id'] == "harbour_selector.value":
        harbour_chosen = None
        click_data = None

    directions = {"Departure":0, "Arrival":1}

    if click_data is None or not region_chosen or not harbour_chosen:
        line_fig_empty = line_charts.get_empty_figure("harbour_page")

        return line_fig_empty
    #
    # num_trips = click_data['points'][0]['y']
    year = click_data['points'][0]['x']
    direction = click_data["points"][0]["customdata"][0]
    trip_direction = directions[direction]

    if not toggle_value:
    # daily trip line chart

        if trip_direction == 0: # departure
            line_data = preprocess.get_depart_by_harbour(trips_df_heat, region_chosen, harbour_chosen)
            line_data = preprocess.prepare_day_month_data_by_harbour(line_data, year, "daily")

        elif trip_direction == 1: # arrive
            line_data = preprocess.get_arrive_by_harbour(trips_df_heat, region_chosen, harbour_chosen)
            line_data = preprocess.prepare_day_month_data_by_harbour(line_data, year, "daily")

        else:
            print("wrong trip direction value")
            return go.Figure(), go.Figure()

        my_fig = line_charts.get_region_figure(line_data,
                                                 region_chosen,
                                                 year,
                                                 trip_direction,
                                                 harbour=harbour_chosen)

    else:
        # monthly trip bar chart

        if trip_direction == 0: # departure
            bar_data = preprocess.get_depart_by_harbour(trips_df_heat, region_chosen, harbour_chosen)
            bar_data = preprocess.prepare_day_month_data_by_harbour(bar_data, year, "monthly")

        elif trip_direction == 1: # arrive
            bar_data = preprocess.get_arrive_by_harbour(trips_df_heat, region_chosen, harbour_chosen)
            bar_data = preprocess.prepare_day_month_data_by_harbour(bar_data, year, "monthly")

        else:
            print("wrong trip direction value")
            return go.Figure(), go.Figure()

        my_fig = bar_charts.get_region_figure(bar_data,
                                                 region_chosen,
                                                 year,
                                                 trip_direction,
                                                 harbour=harbour_chosen)


    return my_fig


# vessel page feature. show heatmap
@app.callback(
    Output("heatmap_vessel", "figure"),
    [Input("vessel_selector", "value")],
)
def updape_heat_by_vessel(vessel_chosen):
    '''
        Based on the vessel type indicated by the dropdown,
        display all trips using the type of vessel on a heatmap.

        Args:
            A value indicates a vessel type.
        Returns:
            A heatmap shows all trips using the type of vessel.
    '''
    trip_direction = 2  # display depart + arrive

    # filter by vessel type, vessel_chosen can never be None, controled by Dash.
    trips_vessel_df = trips_df_heat.loc[trips_df_heat["Vessel Type"]==vessel_chosen]
    yearly_df = preprocess.summarize_yearly_counts(trips_vessel_df, trip_direction)
    data = preprocess.restructure_df(yearly_df)
    region_heat_fig = heatmap.get_figure(data, trip_direction, total_voyage0)

    return region_heat_fig

# vessel page voyage/harbour section.
@app.callback(
    Output('dot_vessel', 'figure'),
    [Input('heatmap_vessel', 'clickData'),
     Input("vessel_selector", "value")]
)
def vessel_heatmap_clicked(click_data, vessel_chosen):
    '''
        The heatmap displays all trips using a type of vessel.
        When a cell in the heatmap is clicked, updates the
        dot plot to show the distribution of trips in harbour for
        a region & year. If there is no data to show,
        displays a message. If vessel type changes, display a message.

        Args:
            The necessary input to update the dot plot.
        Returns:
            The necessary output values to update the dot plot.
    '''
    ctx = dash.callback_context
    my_trigger = ctx.triggered

    if my_trigger[0]["prop_id"] == "vessel_selector.value":
        click_data = None

    if click_data is None or click_data['points'][0]['z'] == None:
        dot_fig_empty = dot_charts.get_empty_figure()
        return dot_fig_empty

    region = click_data['points'][0]['y']
    year = click_data['points'][0]['x']

    # vessel usage in harbours dot plot
    dotplot_data = preprocess.get_vessel_harbour(
        trips_df_heat,
        vessel_chosen,
        region,
        year
    )

    if dotplot_data.shape:
        fig_RHV = dot_charts.get_vesselport_figure(dotplot_data, region, year)
    else:
        fig_RHV = dot_charts.get_empty_figure()


    return fig_RHV



# voyga page features. if trip Id is incorrect. the map is blank with a message.
@app.callback(
    [Output("trip_passage","figure"),
    Output("trip_input", "pattern")],
    [Input("trip_input", "value")],
)
def retrieve_passage(trip_id):
    '''
    display all the passages of a trip on a map.

        Args:
            A trip Id. If the Id is incorrect, display a message.
        Returns:
            A map showing the itinerary of a trip.
    '''

    pattern = str(trip_id)

    trip_id = trip_id
    atrip = detail_df.loc[detail_df.Id == trip_id]  # all ids in trip.csv are in detail_trip.csv

    if atrip.empty:
        pattern = pattern + "_invalid"

        return passage_map.get_empty_figure(), pattern

    else:
        fig = passage_map.get_passage_map(atrip)


    return fig, pattern

