from sqlalchemy import create_engine, Column, Integer, DateTime, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd
from sqlalchemy.orm import sessionmaker
import glob
from datetime import datetime as datetime_module
import numpy as np
import os



def create_findmyride_database(database_name):
    engine = create_engine('postgresql://%s:%s@localhost/%s'%('dianeivy', 'tmp_password', database_name))
    print(engine.url)

    if not database_exists(engine.url):
        create_database(engine.url)
    print(database_exists(engine.url))
    return engine


Base = declarative_base()
class WeatherData(Base):
    __tablename__ = 'weather_merged'

    id = Column(Integer, primary_key=True)
    station_id = Column(String, index=True)
    event_date_weather = Column(DateTime)
    temp_avg = Column(Float)
    precip = Column(Float)

    def __repr__(self):
        return "<WeatherData(station_id='%s', event_date_weather='%s', temp_avg='%f', precip='%f')>"  \
               %(self.station_id, self.event_date_weather, self.temp_avg, self.precip)


def load_hubway_database():
    return psycopg2.connect(database='hubway_db', user='dianeivy', host='localhost', password='tmp_password')


def fill_daily_precip(hourly_row, daily_frame):
    if hourly_row['precip'] is None or str(hourly_row['precip']).lower() == 'nan':
        if any(daily_frame['event_date_weather'].isin([hourly_row['event_date_weather_day']])):
            return daily_frame[(daily_frame['event_date_weather'] == hourly_row['event_date_weather_day'])]['precip'].iloc[0] / 10. * 0.0393701 / 24.
        else:
            return 0.
    else:
        return hourly_row['precip']


def fill_daily_temp(hourly_row, daily_frame):
    if hourly_row['temp_avg'] is None or str(hourly_row['temp_avg']).lower() == 'nan':
        if any(daily_frame['event_date_weather'].isin([hourly_row['event_date_weather_day']])):
            min_temp = daily_frame[(daily_frame['event_date_weather'] == hourly_row['event_date_weather_day'])]['temp_min'].iloc[0]
            max_temp = daily_frame[(daily_frame['event_date_weather'] == hourly_row['event_date_weather_day'])]['temp_max'].iloc[0]
            return (min_temp + max_temp) / 2.
        else:
            return None
    else:
        return hourly_row['temp_avg']



def create_new_dates():
    con = load_hubway_database()
    daily_data = pd.read_sql_query("SELECT * FROM weather", con).fillna(value=0)
    hourly_data = pd.read_sql_query("SELECT * FROM weather_hourly", con)
    print(hourly_data.info())

    daily_hourly_dates = np.sort(list(set(list([datetime_module(tmp_date.year, tmp_date.month, tmp_date.day, hr, 0)
                                                for tmp_date in daily_data['event_date_weather']
                                                for hr in xrange(24)]) + list(hourly_data['event_date_weather']))))
    dates_dataframe = pd.DataFrame(data = {'event_date_weather': daily_hourly_dates})
    dates_dataframe['event_date_weather_day'] = pd.DatetimeIndex(dates_dataframe.event_date_weather).normalize()


    merged_weather_data = pd.merge(dates_dataframe, hourly_data, on='event_date_weather', how='inner')
    print(merged_weather_data.info())
    merged_weather_data['merged_precip'] = merged_weather_data.apply(fill_daily_precip, axis=1, args=[daily_data])
    merged_weather_data['merged_temp'] = merged_weather_data.apply(fill_daily_temp, axis=1, args=[daily_data])
    print merged_weather_data.info()

    return merged_weather_data


def create_weather_table(engine):
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    final_merged_weather = create_new_dates()
    for tmp_date, tmp_temp, tmp_precip  in zip(final_merged_weather['event_date_weather'],
                                                      final_merged_weather['merged_temp'],
                                                      final_merged_weather['merged_precip']):
        print tmp_date, tmp_temp, tmp_precip
        record = WeatherData(**{'station_id': 'boston',
                                'event_date_weather': tmp_date,
                                'temp_avg': [tmp_temp if tmp_temp > -900 else None][0],
                                'precip': [tmp_precip if tmp_precip > -900 else None][0]})
        s.add(record)
        s.commit()
    s.close()


def run_db():
    db_name = 'hubway_db2'
    engine = create_findmyride_database(db_name)
    Base.metadata.create_all(engine)
    create_weather_table(engine)


if __name__ == '__main__':
    run_db()
