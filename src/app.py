
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
import heatmap, line_charts, bar_charts
#
#
trips_filename = "./assets/data/TRIP_NEW.csv" # TRIP_NEW.csv
detail_filename = "./assets/data/TRIP_DETAIL_NEW.csv"

trips_df = pd.read_csv(trips_filename)
detail_df = pd.read_csv(detail_filename)

trips_df_heat = preprocess.convert_dates(trips_df)
trips_df_heat = preprocess.filter_years(trips_df_heat, 2011, 2021)  # to be used in region, harbour, vessel.

# summary panel
total_voyage0 = trips_df_heat.shape[0]
total_voyage = "{:,}".format(total_voyage0)
international_trips = preprocess.get_international_trips(trips_df_heat)
most_used_vessel = trips_df_heat[["Vessel Type", "Id"]].groupby("Vessel Type"
                                                                ).count().sort_values(by="Id", ascending=False).index[0]
trip_duration = preprocess.get_trip_duration(trips_df_heat, total_voyage0)

# region, harbour, vessel
regions_sorted = sorted(detail_df.Region.unique())
vessel_type_sorted = sorted(trips_df_heat["Vessel Type"].unique())
regions_harbours = detail_df[["Region","Hardour"]].groupby(["Region", "Hardour"]).count().reset_index()


template.create_custom_theme()
template.set_default_theme()

# not needed trip_ids = sorted(trips_df["Id"].unique())


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
    html.Header([
        html.H1('Maritime Traffic in Canada'),
        html.H2('From 2011 to 2021 ---- XPERT SOLUTIONS')
    ]),

    # dcc.Store stores the intermediate value
    dcc.Store(id='intermediate-value-region-trip-direction'),

# panel summary
    html.Div([
        html.Div([
            html.Label(
                "Summary statistic of maritime traffic in Cananda from 2011 to 2021.",
                style={"font-size": "medium"},
            ),

            html.Br(),
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
            style={"heigth": "100%",
                   "width": "100%"},
        ),

 # if come back to two columns in summary panel, uncomment below.
        # html.Div([
        #     html.Label(
        #         "TEST TEST TEST",
        #     ),
        # ],
        #     className="box",
        #     style={"heigth": "100%",
        #            "width": "50%",
        #            },
        # )
    ],
    #    className="row",
    ),

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
                html.Br(),
                radio_trip_direction,
                html.Br(),
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
                ]),
            ],
                className="box",
                style={
                    "margin": "2px",
                    "padding-top": "2px",
                    "padding-bottom": "2px",
                    "width": "96%"
                },
            ),

            html.Div([
                html.Br(),
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
                ])
            ],
                className="box",
                style={
                    "margin": "2px",
                    "padding-top": "2px",
                    "padding-bottom": "2px",
                    "width": "96%"
                },
            ),

            html.Div([
                html.Br(),
                html.Div([
                    dcc.Graph(
                        id='bar_region',
                        className='graph',
                        config=dict(
                            scrollZoom=False,
                            showTips=False,
                            showAxisDragHandles=False,
                            doubleClick=False,
                            displayModeBar=False
                        )
                    )
                ])
            ],
                className="box",
                style={
                    "margin": "2px",
                    "padding-top": "2px",
                    "padding-bottom": "2px",
                    "width": "96%"
                },
            ),

        ])
    # harbour page
    elif filter_chosen == 1:
        return html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                                html.Br(),
                                html.P(
                                    "the original design displays long name in 2 lines. Temporarily made the graph to next line."
                                ),
                                html.Div([
                                    "Select a Region",
                                    dcc.Dropdown(id='region_selector', multi=False,
                                                 options=[{'label': x, 'value': x} for x in regions_sorted],
                                                 value="Pacific Region",
                                                 searchable=True,
                                                 clearable=True,
                                                 style={'width': "100%"}, ),
                                ]),

                                html.Br(),
                                html.Div([
                                    'Select a harbour',
                                    dcc.Dropdown(
                                                 id='harbour_selector', multi=False,
                                                 searchable=True,
                                                 placeholder='Select a Region, then a Harbour...',
                                                 clearable=True,
                                                 style={'width': "100%"}, ),
                                ]),
                            ]),
                    ],
                        className="box",
                        style={
                            "margin": "2px",
                            "padding-top": "2px",
                            "padding-bottom": "2px",
                             "width": "40%"},
                    ),

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
                             "width": "98%",
                               },
                    )
            ],
#                className="row",
            ),

            html.Div([
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
                         "width": "96%",
                           },
                ),

                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='bar_harbour_month',
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
                        "width": "96%",
                    },
                ),

            ]),

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
                        "width": "70%"},
                    ),

                    html.Div([
                        html.Label(
                            "A table of two columns",
                        ),
                    ],
                        className="box",
                        style={
                            "margin": "2px",
                            "padding-top": "2px",
                            "padding-bottom": "2px",
                            "heigth": "100%",
                            "width": "30%",
                        },
                    )
                ],
                    className="row",
                ),
# Add an extra Div layer in case we want to move the heatmap to its own block.

        ])
    # voyage page
    else:
        return html.Div([
            html.Div([
                html.Div([
                    html.Br(),
                    html.Label(
                        "Fill in a trip Id. e.g., 23079000000766035, empty map inidcates invalid Id. "
                    ),

                    html.Div([
                        html.Div([
                            # dcc.Dropdown(id='trip_selector', multi=False,
                            #              options=[{'label': x, 'value': x} for x in trip_ids[:4000]],
                            #          #    value=["Special Purpose"],
                            #              searchable=True,
                            #              placeholder='Select a Vessel Type...',
                            #              clearable=True,
                            #              style={'width': "40%"}, ),
                            dcc.Input(id="trip_input", type="text",
                                      value="2079000000818245",
                                      placeholder="string",
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
                                "margin": "2px",
                                "padding-top": "2px",
                                "padding-bottom": "2px",
                                "heigth": "100%",
                                "width": "92%"},
                        ),

                    ]),
                ],
                    className="box",
                    style={
                        "margin": "2px",
                        "padding-top": "2px",
                        "padding-bottom": "2px",
                        "heigth": "100%",
                        "width": "100%"},
                ),
            ],
            ),
            # we have an extra Div layer in case new graph box is needed, clean up later.

        ])


# region page features: show heatmap
@app.callback(
    [Output("heatmap_region", "figure"),
     Output('intermediate-value-region-trip-direction', 'data'),
     ],
    [Input("trip_direction", "value")],
)
def update_region_heat(direction_chosen):
    #print("output to heat, direction_chosen: ", direction_chosen)

    yearly_df = preprocess.summarize_yearly_counts(trips_df_heat, direction_chosen)  # 0 means Departure
    data = preprocess.restructure_df(yearly_df)


    region_heat_fig = heatmap.get_figure(data, direction_chosen, total_voyage0)

    return region_heat_fig, json.dumps(direction_chosen)


# region page features: show line & bar
@app.callback(
    [Output('line_region', 'figure'),
     Output('bar_region', 'figure'),
     ],
    [Input('heatmap_region', 'clickData'),
     Input('intermediate-value-region-trip-direction', 'data')]
)
def region_heatmap_clicked(click_data, stored_direction):
    '''
        When a cell in the heatmap is clicked, updates the
        line chart to show the data for the corresponding
        region & year. If there is no data to show,
        displays a message.

        Args:
            The necessary inputs and states to update the
            line chart.
        Returns:
            The necessary output values to update the line
            chart.
    '''
    if click_data is None or click_data['points'][0]['z'] == 0:
        line_fig_empty = line_charts.get_empty_figure()
        # line_charts.add_rectangle_shape(line_fig_empty)

        bar_fig_empty = bar_charts.get_empty_figure()
    #    bar_charts.add_rectangle_shape(bar_fig_empty)

        return line_fig_empty, bar_fig_empty

    region = click_data['points'][0]['y']
    year = click_data['points'][0]['x']

    get_dcc_store_direction = json.loads(stored_direction)
    #print("Inside heatmap_click | dcc stored radio button direction: ", get_dcc_store_direction)

    # daily trip line chart
    line_data = preprocess.get_data_by_freq(
        trips_df_heat,
        region,
        year,
        get_dcc_store_direction,
        "daily"
    )

    line_fig = line_charts.get_region_figure(line_data, region, year, get_dcc_store_direction)


    # monthly trip bar chart
    bar_data = preprocess.get_data_by_freq(
        trips_df_heat,
        region,
        year,
        get_dcc_store_direction,
        "monthly"
    )

    bar_fig = bar_charts.get_region_figure(bar_data, region, year, get_dcc_store_direction)

    return line_fig, bar_fig


# harbour page features: chained dropdown
@app.callback(
    Output('harbour_selector', 'options'),
    [Input('region_selector', 'value')],
)
def set_harbour_options(region_chosen):
    #print(region_chosen)
    harbours = preprocess.get_harbours_by_region(regions_harbours, region_chosen)

    return [{'label': x, 'value': x} for x in harbours]


# harbour page features: stack bar
@app.callback(
    Output('bar_harbour_year', 'figure'),
    [Input('region_selector', 'value'),
     Input('harbour_selector', 'value')]
)
def add_stack_bar(region, harbour):

    ctx = dash.callback_context
    my_trigger = ctx.triggered
  #  print(my_trigger)

    if my_trigger[0]['prop_id'] == "region_selector.value":
        harbour= None

    if not region or not harbour:
        bar_fig_empty = bar_charts.get_empty_figure()
        # bar_charts.add_rectangle_shape(bar_fig_empty)

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


# harbour page features: click stack bar to show line daily & bar monthly
@app.callback(
    [Output('line_harbour', 'figure'),
     Output('bar_harbour_month', 'figure'),
     ],
    [Input('bar_harbour_year', 'clickData'),
     Input('region_selector', 'value'),
     Input('harbour_selector', 'value')]
)
def region_stack_bar_clicked(click_data, region_chosen, harbour_chosen):
    '''
    curveNumber': 1, departure, the Radio Button value and the stack bar layers are inverse. confusing if use it.
    'curveNumber': 0, arrival
    x: year
    y: number of trips
    '''
   # print(f'click data: {click_data}')

    ctx = dash.callback_context
    my_trigger = ctx.triggered
  #  print(my_trigger)

    if my_trigger[0]['prop_id'] == "region_selector.value" or my_trigger[0]['prop_id'] == "harbour_selector.value":
        harbour_chosen = None
        click_data = None
    #    print("click data should be None")


    directions = {"Departure":0, "Arrival":1}

    if click_data is None or not region_chosen or not harbour_chosen:
        line_fig_empty = line_charts.get_empty_figure()
        # line_charts.add_rectangle_shape(line_fig_empty)

        bar_fig_empty = bar_charts.get_empty_figure()
        # bar_charts.add_rectangle_shape(bar_fig_empty)

        return line_fig_empty, bar_fig_empty
    #
    # num_trips = click_data['points'][0]['y']
    year = click_data['points'][0]['x']
   # trip_direction = click_data["points"][0]["curveNumber"]  # the value is reverse from radio button.
    direction = click_data["points"][0]["customdata"][0]
    trip_direction = directions[direction]


    #print("Inside stack_bar_click | region | harbour ", region_chosen, harbour_chosen)


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

    line_fig = line_charts.get_region_figure(line_data,
                                             region_chosen,
                                             year,
                                             trip_direction,
                                             harbour=harbour_chosen)


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

    bar_fig = bar_charts.get_region_figure(bar_data,
                                             region_chosen,
                                             year,
                                             trip_direction,
                                             harbour=harbour_chosen)



    return line_fig, bar_fig


# vessel page feature. show heatmap
@app.callback(
    Output("heatmap_vessel", "figure"),
    [Input("vessel_selector", "value")],
)
def updape_heat_by_vessel(vessel_chosen):
    trip_direction = 2  # display depart + arrive

    # filter by vessel type, vessel_chosen can never be None, controled by Dash.
    trips_vessel_df = trips_df_heat.loc[trips_df_heat["Vessel Type"]==vessel_chosen]
    yearly_df = preprocess.summarize_yearly_counts(trips_vessel_df, trip_direction)
    data = preprocess.restructure_df(yearly_df)
    region_heat_fig = heatmap.get_figure(data, trip_direction, total_voyage0)

    return region_heat_fig

# vessel page voyage/harbour section. TBD








# voyga page features. if trip Id is incorrect. the map is blank, should return a message.
@app.callback(
    [Output("trip_passage","figure"),
    Output("trip_input", "pattern")],
    [Input("trip_input", "value")],
)
def retrieve_passage(trip_id):
    pattern = trip_id

    trip_id = int(trip_id)
    atrip = detail_df.loc[detail_df.Id == trip_id]  # all ids in trip.csv are in detail_trip.csv

    if atrip.empty:
        pattern = pattern + "_invalid"

    lats = atrip.Latitude
    longs = atrip.Longitude
    fig = px.scatter_mapbox(atrip, lat=lats, lon=longs,
                            hover_data=[atrip["Event Type"], atrip["Rank Number"], atrip.Hardour,
                                        atrip.Region],
                            # color = tst_atrip["Event Type"],
                            zoom=5
                            )
    fig.update_layout(mapbox_style="carto-positron"  # "stamen-toner",
                      )

    fig.update_traces(mode="lines+markers")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
 #   fig.update_layout(height=500, width=800, margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig, pattern
