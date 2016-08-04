import psycopg2
import pandas as pd
import numpy as np
import calendar
from convertdate import holidays


def load_hubway_database():
    return psycopg2.connect(database='hubway_db', user='dianeivy', host='localhost', password='tmp_password')


def find_station_id(con, address_latitude, address_longitude):
    sql_query = "SELECT * FROM station_info;"
    station_info = pd.read_sql_query(sql_query, con)
    station_info['distance'] = ((station_info['latitude'] - address_latitude) * 111.03) ** 2 + \
                               ((station_info['longitude'] - address_longitude) * 85.39) ** 2

    counter = 0
    nearest_stations = []
    for station_id in station_info.sort_values('distance')['station_id']:
        check_station_status = pd.read_sql_query("SELECT * FROM station_statuses WHERE station_id = %d;" %station_id, con)
        if len(check_station_status['event_date']) > 100:
            nearest_stations.append(station_id)
            counter += 1
        if counter == 3:
            break
    for station_id in nearest_stations:
        check_station_status = pd.read_sql_query("SELECT * FROM station_statuses WHERE station_id = %d;" %station_id, con)

    return nearest_stations


def nearby_station_features(con, station_id):
    sql_query = "SELECT * FROM station_info;"
    station_info = pd.read_sql_query(sql_query, con)
    station_lat = station_info[(station_info['station_id'] == station_id)]['latitude'].values[0]
    station_lon = station_info[(station_info['station_id'] == station_id)]['longitude'].values[0]
    station_info['distance'] = ((station_info['latitude'] - station_lat) * 111.03) ** 2 + \
                               ((station_info['longitude'] - station_lon) * 85.39) ** 2

    counter = 0
    nearest_stations = []
    for station_id in station_info.sort_values('distance')['station_id']:
        ## can update this since new count
        check_station_status = pd.read_sql_query("SELECT * FROM station_statuses WHERE station_id = %d;" %station_id, con)
        if len(check_station_status['event_date']) > 100:
            nearest_stations.append(station_id)
            counter += 1
        if counter == 4:
            break

    nearby_station_data = []
    for index, nearby_id in enumerate(nearest_stations[1:]):
        sql_query = "SELECT event_date, num_bikes FROM station_statuses WHERE station_id = %d;" %nearby_id
        tmp_nearby_data = pd.read_sql_query(sql_query, con)
        nearby_station_data.append(pd.DataFrame(data={'event_date': tmp_nearby_data['event_date'],
                                                      'num_bikes_st%d' %(index + 1): tmp_nearby_data['num_bikes']}))

        # print index, nearby_station_data[-1].info()
    return nearby_station_data


def merge_datasets(original_station_data, nearby_station_data):
    final_merged_data = original_station_data
    for index, nearby_df in enumerate(nearby_station_data):
        final_merged_data = pd.merge(final_merged_data, nearby_df.drop_duplicates(), on='event_date')
    return final_merged_data


def holiday_feature(station_data):
    holiday_data = np.zeros((len(station_data['event_date'])))
    # print dir(holidays)

    for index, event_date in enumerate(station_data['event_date']):
        if event_date.month == 1 and event_date.day == 1: holiday_data[index] = 1
        if event_date.month == 1 and event_date.day == 20: holiday_data[index] = 1
        if event_date.month == 7 and event_date.day == 4: holiday_data[index] = 1
        if event_date.month == 11 and event_date.day == 11: holiday_data[index] = 1
        if event_date.month == 12 and event_date.day == 24: holiday_data[index] = 1
        if event_date.month == 12 and event_date.day == 25: holiday_data[index] = 1
        if event_date.month == 12 and event_date.day == 31: holiday_data[index] = 1
        for holiday in [holidays.martin_luther_king_day(event_date.year),
                        holidays.presidents_day(event_date.year),
                        holidays.memorial_day(event_date.year),
                        holidays.labor_day(event_date.year),
                        holidays.columbus_day(event_date.year),
                        holidays.thanksgiving(event_date.year)]:
            if event_date.month == holiday[1] and event_date.day == holiday[2]:
                holiday_data[index] = 1

    station_data['holidays'] = holiday_data
    return station_data


def query_station_status(con, station_id):
    if station_id == 'all':
        sql_query = "SELECT * FROM station_statuses"
    else:
        sql_query = "SELECT * FROM station_statuses WHERE station_id = %d;" %station_id
    return pd.read_sql_query(sql_query, con)


def weather_features(con, station_id):
    if station_id == 'all':
        sql_query = "SELECT * FROM station_statuses JOIN weather_hourly " \
                    "ON date_trunc('hour', station_statuses.event_date) = date_trunc('hour', weather_hourly.event_date_weather)"
    else:
        sql_query = "SELECT * FROM station_statuses JOIN weather_merged ON " \
                    "date_trunc('hour', station_statuses.event_date) = date_trunc('hour', weather_merged.event_date_weather) " \
                    "WHERE station_statuses.station_id = %d" %station_id
        daily_query = "SELECT * FROM station_statuses JOIN weather ON " \
                      "date_trunc('day', station_statuses.event_date) = date_trunc('day', weather.event_date_weather) " \
                      "WHERE station_statuses.station_id = %d" %station_id

    hourly_data = pd.read_sql_query(sql_query, con)
    return hourly_data



def fix_datetimes(station_data):

    def get_hour(val):
        return val * 60

    def get_minute(val):
        return val

    station_data['event_date'] = pd.to_datetime(station_data['event_date'])
    station_data['hour_of_day'] = station_data['event_date'].dt.hour
    station_data['day'] = station_data['event_date'].dt.day
    station_data['minute_of_hour'] = station_data['event_date'].dt.minute
    station_data['day_of_week'] = station_data['event_date'].dt.dayofweek
    station_data['month'] = station_data['event_date'].dt.month
    station_data['minute_of_day'] = station_data['hour_of_day'].apply(get_hour) + station_data['minute_of_hour'].apply(get_minute)

    return station_data


def hubway_station_features(station_id):
    hubway_conn = load_hubway_database()
    hubway_station_data = holiday_feature(fix_datetimes(weather_features(hubway_conn, station_id)))
    nearby_station_data = nearby_station_features(hubway_conn, 3)
    return merge_datasets(hubway_station_data, nearby_station_data)