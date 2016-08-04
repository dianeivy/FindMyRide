from sqlalchemy import create_engine, Column, Integer, DateTime, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd
from sqlalchemy.orm import sessionmaker
import glob
from datetime import date, timedelta, datetime
import numpy as np
import os


## database
def create_findmyride_database(database_name):
    engine = create_engine('postgresql://%s:%s@localhost/%s'%('dianeivy', password, database_name))
    print(engine.url)

    if not database_exists(engine.url):
        create_database(engine.url)
    print(database_exists(engine.url))
    return engine

Base = declarative_base()
class WeatherData(Base):
    __tablename__ = 'weather_hourly'

    id = Column(Integer, primary_key=True)
    station_id = Column(String, index=True)
    event_date_weather = Column(DateTime)
    wind_speed = Column(Float)
    temp_avg = Column(Float)
    precip = Column(Float)

    def __repr__(self):
        return "<WeatherData(station_id='%s', event_date_weather='%s', wind_speed='%f', temp_avg='%f', precip='%f')>"  \
               %(self.station_id, self.event_date_weather, self.wind_speed, self.temp_avg, self.precip)


## load all precip data
def get_precip_data():
    boston_station_id = 190770
    precip_files = ['/Users/dianeivy/Dropbox (MIT)/Insight/Projects/Datasets/Weather_new/precip/3240_%d_2011-2011' %190770] \
                   + glob.glob('/Users/dianeivy/Dropbox (MIT)/Insight/Projects/Datasets/Weather_new/precip/*.dat')

    def load_precip_data(filename):
        with open(filename, 'rb') as file:
            noaa_data = file.readlines()

        precip_units = [line[15:17] for line in noaa_data] ## HI = hundreds of inches
        # print('checking units', set(precip_units))

        precip_dates = []
        precip_data = []
        for line in noaa_data:
            if int(line[3:9]) == boston_station_id:
                precip_year = int(line[17:21])
                precip_month = int(line[21:23])
                precip_day = int(line[23:27])
                for index in np.arange(30, len(line) - 11, 12):
                    precip_hour = int(line[index:index + 2])
                    if precip_hour < 24:
                        precip_data.append(float(line[index + 4: index + 9]) / 100.)
                        precip_dates.append(datetime(precip_year, precip_month, precip_day, precip_hour - 1, 0))

        return precip_dates, precip_data

    all_precip_dates_unsorted = []
    all_precip_data_unsorted = []
    for file in precip_files:
        tmp_dates, tmp_data = load_precip_data(file)
        all_precip_dates_unsorted += tmp_dates
        all_precip_data_unsorted += tmp_data

    date_indices = np.argsort(all_precip_dates_unsorted)
    return np.array(all_precip_dates_unsorted)[date_indices], np.array(all_precip_data_unsorted)[date_indices]


def get_weather_data():

    def load_weather_data(filename):
        with open(filename, 'rb') as file:
            noaa_data = file.readlines()
        all_dates = [datetime(int(line[15:19]), int(line[19:21]), int(line[21:23]), int(line[23:25]), 0) for line in noaa_data]
        wind_speed = [float(line[65:69]) / 10. for line in noaa_data]
        air_temp = [float(line[87:92]) / 10. for line in noaa_data]
        return all_dates, wind_speed, air_temp

    all_weather_dates_unsorted = []
    all_weather_ws_unsorted = []
    all_weather_temp_unsorted = []
    for yr in xrange(2011, 2017):
        tmp_date, tmp_ws, tmp_air = load_weather_data('/Users/dianeivy/Dropbox (MIT)/Insight/Projects/Datasets/Weather_new/temperature/994971-99999-%d' %yr)
        all_weather_dates_unsorted += tmp_date
        all_weather_ws_unsorted += tmp_ws
        all_weather_temp_unsorted += tmp_air

    date_indices = np.argsort(all_weather_dates_unsorted)
    return np.array(all_weather_dates_unsorted)[date_indices], \
           np.array(all_weather_ws_unsorted)[date_indices], \
           np.array(all_weather_temp_unsorted)[date_indices]


def create_weather_table(engine):
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    precip_dates, precip_data = get_precip_data()
    weather_dates, weather_ws, weather_temp = get_weather_data()

    all_dates = np.sort(list(set(list(precip_dates) + list(weather_dates))))
    precip_dates_date = [tmp_date.date() for tmp_date in precip_dates]
    for tmp_date in all_dates:
        if tmp_date in precip_dates:
            precip_val = precip_data[np.argmin(np.abs(tmp_date - precip_dates))]
        elif tmp_date.date() in precip_dates_date:
            precip_val = 0
        else:
            precip_val = None

        if tmp_date in weather_dates:
            ws_val = [weather_ws[np.argmin(np.abs(tmp_date - weather_dates))] if weather_ws[np.argmin(np.abs(tmp_date - weather_dates))] < 990 else None][0]
            temp_val = [weather_temp[np.argmin(np.abs(tmp_date - weather_dates))] if weather_temp[np.argmin(np.abs(tmp_date - weather_dates))] < 990 else None][0]
        else:
            ws_val = None
            temp_val = None

        record = WeatherData(**{'station_id': 'boston',
                                'event_date_weather': tmp_date,
                                'wind_speed': ws_val,
                                'temp_avg': temp_val,
                                'precip': precip_val})
        s.add(record)
        s.commit()
    s.close()


def run_db():
    db_name = 'weather_check'

    engine = create_findmyride_database(db_name)
    Base.metadata.create_all(engine)
    create_weather_table(engine)

if __name__ == '__main__':
    run_db()




