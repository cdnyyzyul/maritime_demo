'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
#from datetime import date

def convert_dates(dataframe):
    '''
        Converts the dates in the dataframe to datetime objects.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with datetime-formatted dates.
    '''
    # Convert dates
    my_df = dataframe[['Id',
                       'Departure Date', 'Departure Hardour', 'Departure Region',
                       'Arrival Date', 'Arrival Hardour', 'Arrival Region', 'Vessel Type']]
    my_df["Departure Date"] = pd.to_datetime(dataframe["Departure Date"], utc=True)
    my_df["Arrival Date"] = pd.to_datetime(dataframe["Arrival Date"], utc=True)
    return my_df


def filter_years(dataframe, start, end):
    '''
        Filters the elements of the dataframe by date, making sure
        they fall in the desired range.

        Args:
            dataframe: The dataframe to process
            start: The starting year (inclusive)
            end: The ending year (inclusive)
        Returns:
            The dataframe filtered by date.
    '''
    # Filter by dates
    gt_start_depart = dataframe["Departure Date"].dt.year >= start
    lt_end_depart = dataframe["Departure Date"].dt.year <= end
    start_end_depart = gt_start_depart & lt_end_depart
    dataframe1 = dataframe.loc[start_end_depart]

    gt_start_arrival = dataframe["Arrival Date"].dt.year >= start
    lt_end_arrival = dataframe["Arrival Date"].dt.year <= end
    start_end_arrival = gt_start_arrival & lt_end_arrival
    my_df = dataframe.loc[start_end_arrival]

    return my_df


def summarize_yearly_counts(dataframe, trip_direction):
    '''
        Groups the data by neighborhood and year,
        summing the number of trees planted in each neighborhood
        each year.

        Args:
            dataframe: The dataframe to process
            trip_direction: departure, arrival, total, 0,1,2
        Returns:
            The processed dataframe with column 'Counts'
            containing the counts of planted
            trees for each neighborhood each year.
    '''
    # Summarize df

    my_df = dataframe.copy()
    if trip_direction == 0:
        # group by year_end on the column "Departure Date", keep Departure Region, no Hardour but vessel page may need it.
        my_df = my_df.groupby([pd.Grouper(key="Departure Date", freq="1Y"),
                               "Departure Region"]).agg(Counts=pd.NamedAgg(column="Departure Region", aggfunc="count"))
    elif trip_direction == 1:
        my_df = my_df.groupby([pd.Grouper(key="Arrival Date", freq="1Y"),
                               "Arrival Region"]).agg(Counts=pd.NamedAgg(column="Arrival Region", aggfunc="count"))
    else:
        my_df0 = my_df.groupby([pd.Grouper(key="Departure Date", freq="1Y"),
                               "Departure Region"]).agg(Counts=pd.NamedAgg(column="Departure Region", aggfunc="count"))
        my_df1 = my_df.groupby([pd.Grouper(key="Arrival Date", freq="1Y"),
                               "Arrival Region"]).agg(Counts=pd.NamedAgg(column="Arrival Region", aggfunc="count"))
        my_df0.index.rename(["Date", "Region"], inplace=True)
        my_df1.index.rename(["Date", "Region"], inplace=True)
        my_df0.reset_index(inplace=True)
        my_df1.reset_index(inplace=True)
        my_dff = my_df0.append(my_df1)
        my_df = my_dff.groupby(['Date', 'Region']).agg(Counts2=pd.NamedAgg(column="Counts", aggfunc="sum"))
        my_df.rename(columns = {"Counts2":"Counts"}, inplace=True)

    my_df.index.rename(["Date", "Region"], inplace=True)

    return my_df


def restructure_df(yearly_df):
    '''
        Restructures the dataframe into a format easier
        to be displayed as a heatmap.

        The resulting dataframe should have as index
        the names of the neighborhoods, while the columns
        should be each considered year. The values
        in each cell represent the number of trees
        planted by the given neighborhood the given year.

        Any empty cells are filled with zeros.

        Args:
            yearly_df: The dataframe to process
        Returns:
            The restructured dataframe
    '''
    # Restructure df and fill empty cells with 0

    my_df = yearly_df.unstack().transpose()
    my_df.rename(columns=lambda i: i.date(), inplace=True)
    my_df = my_df.fillna(0)
    my_df.index = my_df.index.droplevel(0)

    return my_df


def get_data_by_freq(dataframe, region, year, trip_direction, freq):
    '''
        From the given dataframe, gets
        the daily amount of planted trees
        in the given neighborhood and year.

        Args:
            dataframe: The dataframe to process
            arrond: The desired neighborhood
            year: The desired year
        Returns:
            The daily tree count data for that
            neighborhood and year.
    '''
    # define the frequency for daily and monthly.
    frequencies = {"daily" : "1D", "monthly": "MS"}
    interval = frequencies[freq]

    if trip_direction == 0:
        df_year_region = dataframe.loc[(dataframe["Departure Date"].dt.year == year) & (dataframe["Departure Region"] == region)]
        df_freq = df_year_region.groupby(pd.Grouper(key="Departure Date", freq=interval)) \
            .agg(Counts=pd.NamedAgg(column="Departure Region", aggfunc="count"))

    if trip_direction == 1:
        df_year_region = dataframe.loc[(dataframe["Arrival Date"].dt.year == year) & (dataframe["Arrival Region"] == region)]
        df_freq = df_year_region.groupby(pd.Grouper(key="Arrival Date", freq=interval)) \
            .agg(Counts=pd.NamedAgg(column="Arrival Region", aggfunc="count"))

    if trip_direction == 2:
        df_year_region0 = dataframe.loc[(dataframe["Departure Date"].dt.year == year) & (dataframe["Departure Region"] == region)]
        df_freq0 = df_year_region0.groupby(pd.Grouper(key="Departure Date", freq=interval)) \
            .agg(Counts=pd.NamedAgg(column="Departure Region", aggfunc="count"))
        df_year_region1 = dataframe.loc[(dataframe["Arrival Date"].dt.year == year) & (dataframe["Arrival Region"] == region)]
        df_freq1 = df_year_region1.groupby(pd.Grouper(key="Arrival Date", freq=interval)) \
            .agg(Counts=pd.NamedAgg(column="Arrival Region", aggfunc="count"))

        df_freq0.index.rename("Date", inplace=True)
        df_freq1.index.rename("Date", inplace=True)
        df_freq0.reset_index(inplace=True)
        df_freq1.reset_index(inplace=True)

        my_df = df_freq0.append(df_freq1)
        df_freq = my_df.groupby('Date').agg(Counts2=pd.NamedAgg(column="Counts", aggfunc="sum"))
        df_freq.rename(columns = {"Counts2":"Counts"}, inplace=True)


    df_freq.index.rename("Date", inplace=True)
    df_freq.reset_index(inplace=True)
    df_freq.Date = df_freq.Date.dt.date.astype('datetime64')

    return df_freq

def all_region_harbour(dataframe):
    deprhs = dataframe[["Departure Region", "Departure Hardour"]].groupby(
        ["Departure Region", "Departure Hardour"]).count().reset_index()
    arrvrhs = dataframe[["Arrival Region", "Arrival Hardour"]].groupby(
        ["Arrival Region", "Arrival Hardour"]).count().reset_index()
    deprhs.rename(columns={"Departure Region": "Region", "Departure Hardour": "Harbour"}, inplace=True)
    arrvrhs.rename(columns={"Arrival Region": "Region", "Arrival Hardour": "Harbour"}, inplace=True)
    rh = deprhs.append(arrvrhs)
    return rh

def get_depart_by_harbour(dataframe, region, harbour):
    # departure
    depart_hb_rg = dataframe.loc[(dataframe["Departure Region"] == region) &
                                     (dataframe["Departure Hardour"] == harbour)]
    depart_hb_rg = depart_hb_rg[['Id', 'Departure Date']]
    depart_hb_rg["Direction"] = "Departure"
    depart_hb_rg.rename(columns={"Departure Date": "Date"}, inplace=True)

    return depart_hb_rg


def get_arrive_by_harbour(dataframe, region, harbour):
    # arrival
    arrv_hb_rg = dataframe.loc[(dataframe["Arrival Region"] == region) &
                                   (dataframe["Arrival Hardour"] == harbour)]
    arrv_hb_rg = arrv_hb_rg[['Id', 'Arrival Date']]
    arrv_hb_rg["Direction"] = "Arrival"
    arrv_hb_rg.rename(columns={"Arrival Date": "Date"}, inplace=True)

    return arrv_hb_rg

def prepare_day_month_data_by_harbour(dataframe, year, freq):

    frequencies = {"daily" : "1D", "monthly": "MS"}
    interval = frequencies[freq]

    dataframe = dataframe.loc[dataframe.Date.dt.year == year]
    harb_data = dataframe.groupby([pd.Grouper(key="Date", freq=interval)]
                                       ).agg(Counts=pd.NamedAgg(column="Id", aggfunc="count"))
    harb_data.reset_index(inplace=True)

    return harb_data




def prepare_data_by_harbour(depart_hb_rg, arrv_hb_rg):

    # all trips
    trip_hb_rg = depart_hb_rg.append(arrv_hb_rg)

    stack_bar_data = trip_hb_rg.groupby([pd.Grouper(key="Date", freq="1YS"), "Direction"]
                                        ).agg(Counts=pd.NamedAgg(column="Id", aggfunc="count"))
    stack_bar_data.reset_index(inplace=True)

    return stack_bar_data



def get_harbours_by_region(regions_harbours, region):
    harbour_by_region = regions_harbours.loc[regions_harbours.Region == region]["Harbour"].unique()

    return harbour_by_region


def get_international_trips(trips_df):
    total_voyage = trips_df.shape[0]
    east_water = trips_df.loc[(trips_df["Departure Region"] == "East Canadian Water Region") |
                              (trips_df["Arrival Region"] == "East Canadian Water Region")].shape[0]
    west_water = trips_df.loc[(trips_df["Arrival Region"] == "West Canadian Water Region") |
                              (trips_df["Departure Region"] == "West Canadian Water Region")].shape[0]
    international = east_water + west_water
    percentage = round(international / total_voyage * 100, 2)
    percentage = "{:,}".format(percentage) + "%"
    return percentage


def get_hours(td):
  """
  input timedelta
  return number of hours
  """
  return td.days * 24 + round(td.seconds/3600,2)

def get_trip_duration(trips_df, total_voyage):
    duration = trips_df['Arrival Date'] - trips_df['Departure Date']
    duration_hour = duration.apply(get_hours)
    total_duration_hour = duration_hour.sum()
    avg_duration_hour = round(total_duration_hour / total_voyage, 2)
    avg_duration_hour = "{:,}".format(avg_duration_hour)
    return avg_duration_hour

def get_vessel_harbour(trips_df_heat, vessel_chosen, region, year):

    trips_vessel = trips_df_heat.loc[trips_df_heat["Vessel Type"] == vessel_chosen]

    trips_vessel_depart = trips_vessel.loc[(trips_vessel["Departure Date"].dt.year == year) &
                                           (trips_vessel["Departure Region"] == region)][["Departure Hardour"]]
    trips_vessel_depart.rename(columns={"Departure Hardour": "Harbour"}, inplace=True)

    trips_vessel_arrive = trips_vessel.loc[(trips_vessel["Arrival Date"].dt.year == year) &
                                           (trips_vessel["Arrival Region"] == region)][["Arrival Hardour"]]
    trips_vessel_arrive.rename(columns={"Arrival Hardour": "Harbour"}, inplace=True)

    trips_vessel_rh = trips_vessel_depart.append(trips_vessel_arrive)
    trips_vessel_rh = trips_vessel_rh.groupby(["Harbour"]
                                              ).agg(Counts=pd.NamedAgg(column="Harbour", aggfunc="count"),
                                                    ).reset_index()

    trips_vessel_rh_dot_data = trips_vessel_rh.sort_values(by="Counts")

    return trips_vessel_rh_dot_data
